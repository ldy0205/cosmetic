import pandas as pd

# 1. 파일 읽기
file_path = '대한무역투자진흥공사_4대 소비재 국가별 수출금액 (화장품)_20221231.csv'
df = pd.read_csv(file_path)

# 2. 분석용 연도 컬럼 리스트
years = ['2018', '2019', '2020', '2021', '2022']

# 3. 데이터 가공 (상위 20개국 추출 및 통계)
# 2022년 수출액이 높은 순서로 정렬
top_n = df.sort_values(by='2022', ascending=False).head(20).copy()

# 국가별 5개년 총합 및 평균 컬럼 추가
top_n['5개년_총합'] = top_n[years].sum(axis=1)
top_n['5개년_평균'] = top_n[years].mean(axis=1).round(0)

# 4. 결과 출력 (깔끔하게 보기)
print(f"{'국가명':<10} | {'2022년 수출액':>15} | {'5개년 평균':>15}")
print("-" * 50)
for _, row in top_n.iterrows():
    print(f"{row['국가명']:<10} | {row['2022']:>15,.0f} | {row['5개년_평균']:>15,.0f}")

# 5. 분석 데이터 엑셀 파일로 추출 (필요 시 주석 해제)
# top_n.to_excel('화장품_수출_상위20개국_분석.xlsx', index=False)