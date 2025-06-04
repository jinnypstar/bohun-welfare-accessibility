import pandas as pd
import re

# 1. 원본 병원 데이터 불러오기
hospital_df = pd.read_csv("../data/raw/bohun_hospital_all.csv", encoding="utf-8")

# 2. 지역코드 생성: 광역시도명 + 시군구명
hospital_df["지역코드"] = hospital_df["광역시도명"].str.strip() + " " + hospital_df["시군구명"].str.strip()

# 3. 세부 구로 나뉜 시 → 대표 구로 수동 매핑
multi_gu_mapping = {
    "전북특별자치도 전주시": "전북특별자치도 전주시 덕진구",
    "경상북도 포항시": "경상북도 포항시 남구",
    "충청북도 청주시": "충청북도 청주시 상당구",
    "경기도 고양시": "경기도 고양시 덕양구",
    "경기도 부천시": "경기도 부천시 소사구",
    "경기도 성남시": "경기도 성남시 수정구",
    "경기도 수원시": "경기도 수원시 권선구",
    "경기도 안산시": "경기도 안산시 단원구",
    "경기도 안양시": "경기도 안양시 동안구",
    "경기도 용인시": "경기도 용인시 기흥구",
    "충청남도 천안시": "충청남도 천안시 동남구",
    "경상남도 창원시": "경상남도 창원시 마산합포구",
    "세종특별자치시 세종시": "세종특별자치시 도담동"
}

# 4. 중복 구 이름 → 괄호 처리 (ex: 중구(서울))
duplicate_gu = {"중구", "서구", "동구", "남구", "북구", "강서구"}

def apply_standardization(row):
    gu = row["시군구명"].strip()
    metro = row["광역시도명"].strip()
    full = f"{metro} {gu}"
    if full in multi_gu_mapping:
        return multi_gu_mapping[full]
    elif gu in duplicate_gu:
        simplified = re.sub(r"(특별자치도|특별자치시|특별시|광역시|도)$", "", metro).strip()
        return f"{metro} {gu}({simplified})"
    else:
        return full

# 5. 통일지역코드 생성 및 분할
hospital_df["통일지역코드"] = hospital_df.apply(apply_standardization, axis=1)
hospital_df["지역명"] = hospital_df["통일지역코드"].apply(lambda x: x.split()[0])
hospital_df["시군구명2"] = hospital_df["통일지역코드"].apply(lambda x: " ".join(x.split()[1:]))

# 6. 기존 컬럼 삭제
hospital_df = hospital_df.drop(columns=["광역시도명", "시군구명", "지역코드", "통일지역코드"])

# 7. 시군구명2 → 시군구명 으로 이름 변경
hospital_df.rename(columns={"시군구명2": "시군구명"}, inplace=True)

# 8. 저장
hospital_df.to_csv("../data/processed/bohun_hospital_final.csv", index=False, encoding="utf-8-sig")
