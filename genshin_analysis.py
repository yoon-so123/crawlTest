import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.rc('font', family='Malgun Gothic')  # 윈도우의 기본 한글 폰트
plt.rcParams['axes.unicode_minus'] = False     # 마이너스 기호 깨짐 방지

# 1. 데이터 불러오기 및 전처리
df_56 = pd.read_csv('genshin_5.6.csv')
df_57 = pd.read_csv('genshin_5.7.csv')

# 존재하는 컬럼명으로 수정: 'body' → 'content', 'comment' → 'comments'
df_56['text'] = df_56['title'].fillna('') + ' ' + df_56['content'].fillna('') + ' ' + df_56['comments'].fillna('')
df_57['text'] = df_57['title'].fillna('') + ' ' + df_57['content'].fillna('') + ' ' + df_57['comments'].fillna('')

# 2. 감정분석 모델 로딩
model_name = "slave-factory/kobert-emotion-classifier-v3"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, top_k=None)

def analyze_emotion(text):
    try:
        result = classifier(text[:512])[0]  # 긴 텍스트 자르기
        return pd.Series([result['label'], result['score']])
    except Exception:
        return pd.Series(['error', 0])

# 3. 감정분석 적용
# df_56[['label', 'score']] = df_56['text'].apply(analyze_emotion)
# df_57[['label', 'score']] = df_57['text'].apply(analyze_emotion)
# 3. 감정분석 적용 (title 기준만 사용)
def analyze_emotion_title_only(title):
    try:
        result = classifier(title[:512])[0]
        return pd.Series([result['label'], round(result['score'], 4)])
    except Exception:
        return pd.Series(['error', 0])

df_56[['label', 'score']] = df_56['title'].fillna('').apply(analyze_emotion_title_only)
df_57[['label', 'score']] = df_57['title'].fillna('').apply(analyze_emotion_title_only)


# 4. TF-IDF 키워드 추출
def extract_top_keywords(texts, top_n=10):
    vectorizer = TfidfVectorizer(max_features=500)
    tfidf_matrix = vectorizer.fit_transform(texts)
    scores = tfidf_matrix.sum(axis=0).A1
    keywords = [word for word, idx in sorted(vectorizer.vocabulary_.items(), key=lambda x: -scores[x[1]])[:top_n]]
    return keywords

keywords_56 = extract_top_keywords(df_56['text'])
keywords_57 = extract_top_keywords(df_57['text'])

print("🔍 5.6 키워드:", keywords_56)
print("🔍 5.7 키워드:", keywords_57)

# 5. 감정 분포 시각화 저장
def plot_emotion_distribution(df, title, filename):
    sns.countplot(data=df, x='label')
    plt.title(title)
    plt.savefig(filename)
    plt.clf()

plot_emotion_distribution(df_56, "5.6 감정 분포", "emotion_56.png")
plot_emotion_distribution(df_57, "5.7 감정 분포", "emotion_57.png")

# 6. 결과 저장
df_56.to_csv("result_5_6.csv", index=False)
df_57.to_csv("result_5_7.csv", index=False)

print("✅ 감정분석 완료. 결과가 result_5_6.csv, result_5_7.csv 에 저장되었습니다.")
