import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. 페이지 제목 설정
st.set_page_config(page_title="농수산물 양허세율 조회", layout="wide")
st.title("🌾 국영무역품목 양허세율 데이터 분석")

# 2. 파일 자동 찾기 (파일명 직접 입력 안 함 - 에러 방지 핵심)
def get_data_file():
    for f in os.listdir('.'):
        if "양허세율" in f and f.endswith(".csv"):
            return f
    return None

data_file = get_data_file()

# 3. 데이터 로드 함수
@st.cache_data
def load_data(file_path):
    if not file_path:
        return None
    try:
        # 다양한 한글 인코딩 방식 순차 시도
        for enc in ['cp949', 'utf-8-sig', 'euc-kr']:
            try:
                df = pd.read_csv(file_path, encoding=enc)
                # 컬럼명에 있는 공백이나 특수문자 제거
                df.columns = df.columns.str.strip()
                return df
            except:
                continue
    except Exception as e:
        st.error(f"데이터 로딩 실패: {e}")
    return None

df = load_data(data_file)

# 4. 화면 구성
if df is not None:
    st.success(f"✅ 파일을 성공적으로 찾았습니다: `{data_file}`")
    
    # 숫자 데이터 정제 (콤마 제거 등)
    for col in ['저율관세(추천, %)', '고율종가(미추천)']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)

    # 사이드바 필터링
    items = df['품명'].unique()
    selected = st.sidebar.multiselect("조회할 품목을 선택하세요", items, default=items)
    filtered_df = df[df['품명'].isin(selected)]

    # 차트 그리기
    st.subheader("📊 품목별 세율 비교 (저율 vs 고율)")
    fig = px.bar(filtered_df, x='품명', y=['저율관세(추천, %)', '고율종가(미추천)'], barmode='group')
    st.plotly_chart(fig, use_container_width=True)

    # 데이터 표 출력
    st.subheader("📋 전체 데이터 내역")
    st.dataframe(filtered_df)
else:
    st.error("❌ 서버에서 CSV 파일을 찾을 수 없습니다.")
    st.info("GitHub 저장소의 첫 화면(Root)에 CSV 파일이 잘 올라와 있는지 확인해 주세요.")
    st.write("현재 서버 파일 목록:", os.listdir('.'))