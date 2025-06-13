import pandas as pd

# 1. 두 CSV 불러오기
df1 = pd.read_csv("원신_5.6_유저반응_크롤링.csv", encoding='utf-8-sig')
df2 = pd.read_csv("원신_5.6_유저반응_크롤링_100개.csv", encoding='utf-8-sig')

# 2. 합치기 (중복 제거 포함)
merged_df = pd.concat([df1, df2], ignore_index=True)
merged_df = merged_df.drop_duplicates(subset=['title', 'content'], keep='first')

# 3. 저장
merged_df.to_csv("원신_5.6_유저반응_통합.csv", index=False, encoding='utf-8-sig')

print("✅ 병합 완료: '원신_5.6_유저반응_통합.csv' 생성됨")
