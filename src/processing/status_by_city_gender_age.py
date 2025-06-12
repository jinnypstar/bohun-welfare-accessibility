import pandas as pd

# 📁 엑셀 파일 경로
file_path = "../data/raw/bohun_status_by_city_gender_age.xlsx"

# 📊 연령 칼럼 정의
ages_all = [f"{i}세" for i in range(0, 100)] + ['100세 이상']
ages_old = [f"{i}세" for i in range(65, 100)] + ['100세 이상']
cols_needed = ['시도', '시군구'] + ages_all

# ✅ 필요한 컬럼만 읽기
df = pd.read_excel(file_path, usecols=cols_needed)

# 🔄 문자열 → 숫자 변환 (에러 방지용)
for col in ages_all:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 👴 고령자수 & 📈 전체 보훈대상자수 계산
df['고령자수'] = df[ages_old].sum(axis=1, skipna=True)
df['보훈대상자수'] = df[ages_all].sum(axis=1, skipna=True)

# 📍 시도/시군구별로 합치기
summary = df.groupby(['시도', '시군구'])[['보훈대상자수', '고령자수']].sum().reset_index()

# 💾 저장
summary.to_excel("../data/processed/bohun_summary_by_city.xlsx", index=False)
