import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. 페이지 설정
st.set_page_config(page_title="화장품 수출 데이터 분석", layout="wide")

st.title("💄 국가별 화장품 수출 금액 분석 대시보드")
st.markdown("K-뷰티의 국가별 수출 추이를 연도별(2018-2022)로 분석합니다.")

# 2. 파일 경로 설정 (정확한 파일명)
data = "대한무역투자진흥공사_4대 소비재 국가별 수출금액 (화장품)_20221231.csv"

@st.cache_data
def load_data(file_path):
    # 만약 지정된 파일명이 없으면 폴더 내의 다른 CSV를 자동으로 찾음
    if not os.path.exists(file_path):
        all_files = os.listdir('.')
        csv_files = [f for f in all_files if f.endswith('.csv')]
        if csv_files:
            file_path = csv_files[0] # 첫 번째 발견된 CSV 사용
        else:
            return None

    try:
        # 인코딩 시도 (공공데이터는 보통 cp949)
        try:
            df = pd.read_csv(file_path, encoding='cp949')
        except:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
        
        # 컬럼명 앞뒤 공백 제거
        df.columns = df.columns.str.strip()
        
        # 숫자 데이터 정제: 콤마(,) 제거 및 숫자 변환
        year_cols = ['2018', '2019', '2020', '2021', '2022']
        for col in year_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return None

# 데이터 실행
df = load_data(data)

if df is not None:
    # --- 사이드바 필터 ---
    st.sidebar.header("🔍 분석 조건")
    all_countries = sorted(df['국가명'].unique())
    selected_countries = st.sidebar.multiselect(
        "국가 선택 (복수 선택 가능)", 
        all_countries, 
        default=["중국", "미국", "일본", "베트남"] if "중국" in all_countries else all_countries[:5]
    )

    # 데이터 필터링
    filtered_df = df[df['국가명'].isin(selected_countries)]

    # --- 메인 화면 시각화 ---
    # 1. 연도별 수출 추이 (Line Chart)
    st.subheader("📈 국가별 수출액 변동 추이 (2018 - 2022)")
    
    # 그래프를 그리기 위해 데이터 구조 변경 (Melt)
    melted_df = filtered_df.melt(id_vars='국가명', value_vars=['2018', '2019', '2020', '2021', '2022'],
                                 var_name='연도', value_name='수출금액(USD)')
    
    fig_line = px.line(melted_df, x='연도', y='수출금액(USD)', color='국가명', markers=True,
                       title="연도별 수출액 변화")
    st.plotly_chart(fig_line, use_container_width=True)

    # 2. 2022년 기준 수출 규모 비교 (Bar Chart)
    st.divider()
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 2022년 수출액 비교")
        fig_bar = px.bar(filtered_df.sort_values(by='2022', ascending=False), 
                         x='국가명', y='2022', color='국가명', text_auto=True)
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col2:
        st.subheader("📋 선택 국가 상세 데이터")
        st.dataframe(filtered_df, use_container_width=True)

else:
    st.error(f"❌ '{data}' 파일을 찾을 수 없습니다.")
    st.info("GitHub 저장소의 최상위 폴더에 CSV 파일을 업로드했는지 확인해 주세요.")
    st.write("현재 서버 내 파일 목록:", os.listdir('.'))