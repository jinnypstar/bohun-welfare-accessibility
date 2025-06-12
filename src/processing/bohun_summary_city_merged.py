import pandas as pd

# 1. 원본 파일 경로
file_path = "../data/processed/bohun_summary_by_city.xlsx"  # 경로 필요 시 수정
df = pd.read_excel(file_path)

# 2. 병합할 시군구 목록 정의
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
        "고운동", "금남면", "나성동", "대평동", "도담동", "반곡동", "보람동", "부강면",
        "산울동", "새롬동", "소담동", "소정면", "아름동", "어진동", "연기면", "연동면",
        "연서면", "장군면", "전동면", "전의면", "조치원읍", "종촌동", "집현동", "한솔동", "해밀동"
    ]
}

# 3. 병합 수행
for merged_name, parts in merge_map.items():
    matching_rows = df[df["시군구"].isin(parts)]
    if not matching_rows.empty:
        first_index = matching_rows.index[0]
        new_row = {
            "시도": matching_rows["시도"].iloc[0],
            "시군구": merged_name,
            "보훈대상자수": matching_rows["보훈대상자수"].sum(),
            "고령자수": matching_rows["고령자수"].sum()
        }
        # 원래 시군구 제거 후 새 행 삽입
        df = df[~df["시군구"].isin(parts)]
        df = pd.concat([
            df.iloc[:first_index],
            pd.DataFrame([new_row]),
            df.iloc[first_index:]
        ], ignore_index=True)

# 4. 결과 저장
output_path = "../data/processed/bohun_summary_city_merged.xlsx"
df.to_excel(output_path, index=False)
