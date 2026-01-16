import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. 페이지 설정
st.set_page_config(page_title="농수산물 양허세율 분석", layout="wide")

st.title("🌾 국영무역품목 양허세율 대시보드")
st.markdown("---")

# 2. 파일 자동 감지 로직 (파일명 직접 입력 안 함)
def find_data_file():
    files = os.listdir('.')
    for f in files:
        # 파일명에 '양허세율'이 포함되어 있거나, 업로드하신 특정 키워드가 있는지 확인
        if ("양허세율" in f or "20200925" in f) and f.endswith(".csv"):
            return f
    return None

data_file = find_data_file()

@st.cache_data
def load_and_clean(file_path):
    if not file_path:
        return None
    
    # 여러 인코딩 방식을 순차적으로 시도 (한글 깨짐 방지)
    encodings = ['cp949', 'utf-8-sig', 'euc-kr', 'utf-8']
    df = None
    
    for enc in encodings:
        try:
            df = pd.read_csv(file_path, encoding=enc)
            break
        except:
            continue
            
    if df is not None:
        # 컬럼명 앞뒤 공백 제거
        df.columns = df.columns.str.strip()
        # 숫자 데이터에서 콤마 제거 및 수치화
        for col in ['저율관세(추천, %)', '고율종가(미추천)', '종량(미추천, 원/kg)']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        return df
    return None

df = load_and_clean(data_file)

# 3. 화면 렌더링
if df is not None:
    st.success(f"📂 데이터를 성공적으로 불러왔습니다! (파일명: {data_file})")
    
    # 사이드바 필터
    items = df['품명'].unique()
    selected = st.sidebar.multiselect("분석할 품목 선택", items, default=items)
    filtered_df = df[df['품명'].isin(selected)]

    # 차트 출력
    st.subheader("📊 관세율 비교")
    fig = px.bar(
        filtered_df, x='품명', y=['저율관세(추천, %)', '고율종가(미추천)'],
        barmode='group', labels={'value': '세율(%)', 'variable': '구분'}
    )
    st.plotly_chart(fig, use_container_width=True)

    # 데이터 테이블
    st.subheader("📋 전체 데이터 내역")
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.error("❌ 서버에서 CSV 파일을 찾지 못했습니다.")
    st.info("GitHub 저장소 메인 화면에 CSV 파일이 잘 올라가 있는지 확인해 주세요.")
    st.write("현재 폴더 파일 목록:", os.listdir('.'))