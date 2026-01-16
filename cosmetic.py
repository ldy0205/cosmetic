import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. 페이지 설정
st.set_page_config(page_title="농수산물 양허세율 대시보드", layout="wide")

st.title("🌾 국영무역품목 양허세율 분석 서비스")
st.markdown("---")

# 2. 파일 자동 찾기 로직 (파일명 에러 방지)
# 폴더 내 파일들 중 '양허세율'이 포함된 CSV 파일을 자동으로 찾습니다.
current_files = os.listdir('.')
target_file = None

for f in current_files:
    if "양허세율" in f and f.endswith(".csv"):
        target_file = f
        break

@st.cache_data
def load_and_clean_data(file_path):
    if not file_path:
        return None
    
    try:
        # 한국어 인코딩 문제 해결을 위한 시도
        try:
            df = pd.read_csv(file_path, encoding='cp949')
        except:
            df = pd.read_csv(file_path, encoding='utf-8-sig')

        # 컬럼명 공백 제거
        df.columns = df.columns.str.strip()
        
        # 숫자 데이터 정제 (콤마 제거 및 형변환)
        numeric_cols = ['저율관세(추천, %)', '고율종가(미추천)', '종량(미추천, 원/kg)']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
                
        return df
    except Exception as e:
        st.error(f"데이터 정제 중 오류 발생: {e}")
        return None

# 데이터 로드
df = load_and_clean_data(target_file)

# 3. 화면 렌더링
if df is not None:
    st.success(f"✅ 성공적으로 파일을 불러왔습니다: `{target_file}`")
    
    # 사이드바 필터
    st.sidebar.header("🔍 필터")
    items = df['품명'].unique()
    selected = st.sidebar.multiselect("품목 선택", items, default=items)
    
    filtered_df = df[df['품명'].isin(selected)]

    # 그래프 출력
    st.subheader("📊 관세율 비교 (추천 vs 미추천)")
    fig = px.bar(
        filtered_df, 
        x='품명', 
        y=['저율관세(추천, %)', '고율종가(미추천)'],
        barmode='group',
        labels={'value': '세율 (%)', 'variable': '구분'},
        color_discrete_map={'저율관세(추천, %)': '#3498db', '고율종가(미추천)': '#e74c3c'},
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # 테이블 출력
    st.subheader("📋 데이터 상세 내역")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.error("❌ 서버에서 CSV 파일을 찾을 수 없습니다.")
    st.info("GitHub 저장소에 CSV 파일이 업로드되어 있는지 꼭 확인해 주세요!")
    st.write("현재 서버 내 파일 목록:", current_files)