import pandas as pd

# 1. 데이터 불러오기
file_path = '대한무역투자진흥공사_4대 소비재 국가별 수출금액 (화장품)_20221231.csv'
df = pd.read_csv(file_path)

# 2. 전처리: 연도 컬럼 설정
years = ['2018', '2019', '2020', '2021', '2022']

# 3. 주요 분석 결과 생성
# - 연도별 총 합계
yearly_total = df[years].sum().reset_index()
yearly_total.columns = ['연도', '총수출액(USD)']

# - 2022년 기준 상위 10개국 및 성장률(2018 대비 2022) 계산
top_10 = df.sort_values(by='2022', ascending=False).head(10).copy()
top_10['성장률(%)'] = ((top_10['2022'] - top_10['2018']) / top_10['2018'] * 100).round(1)

# 4. 결과 출력
print("        [ 연도별 수출 규모 ]")
print(yearly_total.to_string(index=False))
print("\n" + "="*50)
print("     [ 2022년 수출 상위 10개국 현황 ]")
print(top_10[['국가명', '2022', '성장률(%)']].to_string(index=False))

# 5. 분석 결과 엑셀로 저장 (필요 시 사용)
# top_10.to_excel('화장품_수출_상위국가_분석.xlsx', index=False)
# print("\n✔ '화장품_수출_상위국가_분석.xlsx' 파일로 저장되었습니다.")