import pandas as pd

# 1. 일반 병원 이용률
df1 = pd.read_csv("../data/raw/hospital_utilization_rate.csv", encoding="cp949")
df1.to_excel("../data/raw/hospital_utilization_rate.xlsx", index=False)

# 2. 지정 병원 이용률
df2 = pd.read_csv("../data/raw/designated_hospital_utilization_rate.csv", encoding="cp949")
df2.to_excel("../data/raw/designated_hospital_utilization_rate.xlsx", index=False)
