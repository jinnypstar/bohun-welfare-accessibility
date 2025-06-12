import pandas as pd

# 📁 엑셀 파일 경로
file_path = "../data/processed/bohun_final_df_접근성추가_2.xlsx"
df = pd.read_excel(file_path)

# 🧩 병합할 시군구 정의
merge_map = {
    "전주시": ["전주시 덕진구", "전주시 완산구"],
    "포항시": ["포항시 남구", "포항시 북구"],
    "청주시": ["청주시 상당구", "청주시 서원구", "청주시 청원구", "청주시 흥덕구"],
    "고양시": ["고양시 덕양구", "고양시 일산동구", "고양시 일산서구"],
    "부천시": ["부천시 소사구", "부천시 오정구", "부천시 원미구"],
    "성남시": ["성남시 분당구", "성남시 수정구", "성남시 중원구"],
    "수원시": ["수원시 권선구", "수원시 영통구", "수원시 장안구", "수원시 팔달구"],
    "안산시": ["안산시 단원구", "안산시 상록구"],
    "안양시": ["안양시 동안구", "안양시 만안구"],
    "용인시": ["용인시 기흥구", "용인시 수지구", "용인시 처인구"],
    "천안시": ["천안시 동남구", "천안시 서북구"],
    "창원시": ["창원시 마산합포구", "창원시 마산회원구", "창원시 성산구", "창원시 의창구", "창원시 진해구"],
    "세종특별자치시": [
        "고운동", "금남면", "나성동", "다정동", "대평동", "도담동", "반곡동", "보람동",
        "부강면", "산울동", "새롬동", "소담동", "소정면", "아름동", "어진동", "연기면",
        "연동면", "연서면", "장군면", "전동면", "전의면", "조치원읍", "종촌동",
        "집현동", "한솔동", "해밀동"
    ]
}

# 🔁 인덱스 초기화
df.reset_index(drop=True, inplace=True)

# 병합 처리 (원래 첫 번째 시군구 위치 유지)
for new_name, parts in merge_map.items():
    part_rows = df[df["시군구명"].isin(parts)]
    if not part_rows.empty:
        first_index = part_rows.index[0]
        new_row = {
            "지역명": part_rows["지역명"].iloc[0],
            "시군구명": new_name,
            "병원 수 평균": part_rows["병원 수 평균"].sum(),
            "평균 진료과수": part_rows["평균 진료과수"].sum(),
            "보훈대상자수": part_rows["보훈대상자수"].sum(),
            "고령자비율": part_rows["고령자비율"].mean(),
            "병원/대상자수": part_rows["병원/대상자수"].mean(),
            "보훈대상자 이용률": part_rows["보훈대상자 이용률"].mean(),
            "접근성(분)": part_rows["접근성(분)"].mean()
        }
        df = df[~df["시군구명"].isin(parts)]
        upper = df.iloc[:first_index]
        lower = df.iloc[first_index:]
        df = pd.concat([upper, pd.DataFrame([new_row]), lower], ignore_index=True)

# ✅ 컬럼 삭제: 3,4,6,7,9번째 (0-indexed → 2,3,5,6,8)
cols_to_drop = df.columns[[2, 3, 5, 6, 8]]
df = df.drop(columns=cols_to_drop)

# ✅ 고령자수 컬럼 추가 (보훈대상자수의 15%)
df['고령자수'] = (df['보훈대상자수'] * 0.15).round().astype(int)

# 💾 저장
df.to_excel("../data/processed/city_merged.xlsx", index=False)
