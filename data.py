# 텍스트 처리
import pandas as pd
import re
from collections import Counter

# 형태소 분석기 (명사 추출)
from konlpy.tag import Okt

# 시각화
import matplotlib.pyplot as plt
from wordcloud import WordCloud
# -----------------------------------------
# 1. 데이터 로딩
# -----------------------------------------

# 데이터 불러오기
df = pd.read_csv("dcinside_posts.csv")

# 모든 텍스트 결합
all_text = df['title'].fillna('') + ' ' + df['content'].fillna('') + ' ' + df['comments'].fillna('')
all_text = ' '.join(all_text.tolist())

# 형태소 분석
okt = Okt()
nouns = okt.nouns(all_text)

# 한 글자 제외하고 상위 키워드 추출
filtered = [n for n in nouns if len(n) > 1]
counter = Counter(filtered)
top_keywords = counter.most_common(50)

# 출력
print("📌 상위 50개 키워드:")
for word, freq in top_keywords:
    print(f"{word}: {freq}")
# 워드클라우드 생성