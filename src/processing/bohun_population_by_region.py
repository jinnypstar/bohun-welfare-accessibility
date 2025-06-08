import pandas as pd
import os

data_dir = "../data/raw/bohun_personnel/"
file_list = [
    os.path.join(data_dir, f)
    for f in os.listdir(data_dir)
    if f.endswith(".csv") and f.startswith("veterans_")
]

print("📂 총 파일 수:", len(file_list))

merged_df = pd.DataFrame()

for file in file_list:
    try:
        # 인코딩 자동 처리
        try:
            df = pd.read_csv(file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file, encoding='cp949')

        # 컬럼 순서 기반으로 필요한 3개 컬럼만 선택
        df_selected = df.iloc[:, [1, 2, 6]]
        df_selected.columns = ['지역명', '시군구명', '보훈대상자수']

        # 같은 시군구명끼리 합산
        grouped = df_selected.groupby(['지역명', '시군구명'], as_index=False)['보훈대상자수'].sum()

        # 통합
        merged_df = pd.concat([merged_df, grouped], ignore_index=True)

    except Exception as e:
        print(f"❌ {file} 처리 중 오류:", e)

# ✅ 지역명과 시군구명이 같은 행 제거
before = len(merged_df)
merged_df = merged_df[merged_df['지역명'] != merged_df['시군구명']]
after = len(merged_df)
print(f"🧹 삭제된 행 수: {before - after}")

# 저장
output_path = "../data/processed/veteran_population_by_region.csv"
merged_df.to_csv(output_path, index=False, encoding='utf-8-sig')
print("✅ 저장 완료:", output_path)
