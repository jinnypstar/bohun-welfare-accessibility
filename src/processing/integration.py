import pandas as pd
import re

# 🔹 파일 경로
city_path = "../data/processed/city_merged.xlsx"
hospital_path = "../data/raw/designated_hospital_utilization_rate.xlsx"

# 🔹 파일 불러오기
city_df = pd.read_excel(city_path)
hospital_df = pd.read_excel(hospital_path)

# 🔹 기간 필터링 (2024.05 ~ 2025.04)
hospital_df['년월'] = pd.to_datetime(hospital_df['년월'], format="%Y-%m")
hospital_df = hospital_df[
    (hospital_df['년월'] >= '2024-05-01') & (hospital_df['년월'] <= '2025-04-30')
]

# 🔹 시도명 매핑 (전라북도 → 전북특별자치도 등)
sido_mapping = {
    '서울시': '서울특별시',
    '부산시': '부산광역시',
    '대구시': '대구광역시',
    '인천시': '인천광역시',
    '광주시': '광주광역시',
    '대전시': '대전광역시',
    '울산시': '울산광역시',
    '세종': '세종특별자치시',
    '경기': '경기도',
    '강원도': '강원특별자치도',
    '강원특별자치도': '강원특별자치도',
    '충북': '충청북도',
    '충남': '충청남도',
    '전북': '전북특별자치도',
    '전남': '전라남도',
    '경북': '경상북도',
    '경남': '경상남도',
    '제주도': '제주특별자치도'
}


# 🔹 병합 키 생성 함수 (괄호는 비교만에서 제거, 실제 문자열은 유지)
def create_merge_key(full_name):
    parts = full_name.strip().split()
    if len(parts) < 2:
        return None
    sido_raw = parts[0]
    gu_raw = ' '.join(parts[1:])
    sido = sido_mapping.get(sido_raw, sido_raw)
    gu = re.split(r'\(', gu_raw)[0].strip()
    return f"{sido} {gu}"

# 🔹 designated 데이터: 시군구별 평균 계산 후 병합키 생성
avg_utilization = (
    hospital_df.groupby('시군구')['인원']
    .mean()
    .reset_index()
)
avg_utilization['병합키'] = avg_utilization['시군구'].apply(create_merge_key)

# 🔹 city 데이터: 병합키 생성 (괄호 포함 실제값 유지)
city_df['시군구명_정제'] = city_df['시군구명'].apply(lambda x: re.split(r'\(', str(x))[0].strip())
city_df['병합키'] = city_df['지역명'].str.strip() + " " + city_df['시군구명_정제']

# 🔹 병합 (city 기준)
merged_df = pd.merge(
    city_df,
    avg_utilization[['병합키', '인원']].rename(columns={'인원': '병원 이용자수 평균'}),
    on='병합키',
    how='left'
)

# 🔹 최종 정렬 및 컬럼 선택
final_df = merged_df.sort_values(by=['지역명', '시군구명']).reset_index(drop=True)

# 🔹 필요 시 저장
final_df.to_excel("../data/processed/city_with_utilization.xlsx", index=False)

# 🔹 결과 확인 (예시)
print(final_df[['지역명', '시군구명', '병원 이용자수 평균']].head(15))
