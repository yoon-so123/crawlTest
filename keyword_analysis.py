import pandas as pd
import re
from collections import Counter

# 불용어 리스트
stopwords = ['는', '이', '가', '을', '를', '에', '도', '과', '와', '하다', '합니다', '있다', '없다', '그리고']

def preprocess_and_tokenize(text):
    text = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', text)
    tokens = text.split()
    tokens = [word for word in tokens if word not in stopwords and len(word) > 1]
    return tokens

def extract_top_keywords(csv_path, column_name, top_n=20, encoding='utf-8'):
    df = pd.read_csv(csv_path, encoding=encoding)
    texts = df[column_name].astype(str)
    
    all_words = []
    for sentence in texts:
        all_words.extend(preprocess_and_tokenize(sentence))
    
    word_counts = Counter(all_words)
    top_keywords = word_counts.most_common(top_n)
    
    # DataFrame으로 변환
    result_df = pd.DataFrame(top_keywords, columns=['keyword', 'count'])
    return result_df

# 5.6 버전 키워드 추출
top_56 = extract_top_keywords('genshin_5.6.csv', 'comments')
top_56.to_csv('top_keywords_5_6.csv', index=False, encoding='utf-8-sig')

# 5.7 버전 키워드 추출
top_57 = extract_top_keywords('genshin_5.7.csv', 'comments')
top_57.to_csv('top_keywords_5_7.csv', index=False, encoding='utf-8-sig')
