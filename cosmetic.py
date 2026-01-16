import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 데이터 로드 및 확인
file_name = '대한무역투자진흥공사_4대 소비재 국가별 수출금액 (화장품)_20221231.csv'
df = pd.read_csv(file_name)

# 2. 데이터 전처리
# 연도 컬럼 리스트
years = ['2018', '2019', '2020', '2021', '2022']

# 3. 주요 분석 수행
# (1) 연도별 총 수출액 계산 (단위: 억 달러로 변환하여 가독성 높임)
yearly_summary = df[years].sum() / 100_000_000 

# (2) 2022년 기준 상위 10개국 추출
top_10_2022 = df.nlargest(10, '2022')

# 4. 시각화 설정 (한글 폰트 설정이 필요할 수 있습니다)
plt.rcParams['font.family'] = 'Malgun Gothic' # 윈도우 기준, 맥은 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False
sns.set_palette("husl")

# 그래프 생성
fig, ax = plt.subplots(2, 1, figsize=(12, 12))

# 그래프 1: 연도별 전 세계 총 수출액 추이 (Line Chart)
sns.lineplot(x=yearly_summary.index, y=yearly_summary.values, marker='s', ax=ax[0], color='navy', linewidth=2)
ax[0].set_title('연도별 K-뷰티 총 수출액 추이 (2018-2022)', fontsize=15, pad=15)
ax[0].set_ylabel('수출 금액 (억 달러)')
ax[0].grid(True, linestyle='--', alpha=0.6)

# 그래프 2: 2022년 수출 상위 10개국 비중 (Bar Chart)
sns.barplot(data=top_10_2022, x='2022', y='국가명', ax=ax[1])
ax[1].set_title('2022년 화장품 수출 상위 10개국', fontsize=15, pad=15)
ax[1].set_xlabel('수출 금액 (USD)')

plt.tight_layout()
plt.show()

# 5. 분석 결과 리포트 출력
print("="*50)
print(f"[{years[-1]}년 분석 요약]")
print(f"전체 수출 국가 수: {len(df)}개국")
print(f"최대 수출국: {top_10_2022.iloc[0]['국가명']} ({top_10_2022.iloc[0]['2022']:,} USD)")
print(f"상위 5개국 집중도: {(top_10_2022.head(5)['2022'].sum() / df['2022'].sum() * 100):.1f}%")
print("="*50)