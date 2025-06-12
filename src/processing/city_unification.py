import pandas as pd
import re

# 1. 파일 불러오기
df_summary = pd.read_excel("../data/processed/bohun_summary_city_merged.xlsx")
df_city = pd.read_excel("../data/processed/city_merged.xlsx")

# 2. 컬럼명 맞추기
df_summary = df_summary.rename(columns={"시도": "지역명", "시군구": "시군구명"})

# 3. 시군구명에서 핵심 단어 추출 함수
def extract_core_region(name):
    name = re.sub(r"\(.*?\)", "", str(name))  # 괄호 제거
    match = re.search(r"[\w\d]+[시군구]", name)
    return match.group() if match else name.strip()

# 4. 핵심 시군구명 컬럼 생성
df_city["핵심시군구명"] = df_city["시군구명"].apply(extract_core_region)
df_summary["핵심시군구명"] = df_summary["시군구명"].apply(extract_core_region)

# 5. 병합 (지역명 + 핵심시군구명 기준)
df_merge = pd.merge(
    df_city,
    df_summary[["지역명", "핵심시군구명", "보훈대상자수", "고령자수"]],
    on=["지역명", "핵심시군구명"],
    how="left"
)

# 6. 임시 컬럼 제거
df_merge = df_merge.drop(columns=["핵심시군구명"])

# 7. 덮어쓰기 저장
df_merge.to_excel("../data/processed/city_merged.xlsx", index=False)

