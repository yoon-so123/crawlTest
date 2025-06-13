import pandas as pd
from transformers import pipeline

# 1. 파일 불러오기
df_56 = pd.read_csv("원신_5.6_유저반응_통합.csv", encoding='utf-8-sig')
df_57 = pd.read_csv("원신_5.7_유저반응_크롤링.csv", encoding='utf-8-sig')  # 파일명 수정 필요 시 반영

# 2. 텍스트 컬럼 생성
def merge_text(row):
    return f"{row['title']} {row['content']} {row['comments']}"

df_56['text'] = df_56.apply(merge_text, axis=1)
df_57['text'] = df_57.apply(merge_text, axis=1)

# 3. Hugging Face 감정 분석 파이프라인 로드
emotion_classifier = pipeline(
    "text-classification",
    model="slave-factory/kobert-emotion-classifier-v3",
    top_k=1,
    device=-1  # GPU 사용 시 device=0
)

# 4. 감정 분석 적용 (512자 이하로 자르기)
def get_emotion(text):
    result = emotion_classifier(text[:512])[0][0]
    return pd.Series([result['label'], result['score']])

# 5. 각 데이터프레임에 감정 라벨과 점수 추가
df_56[['label', 'score']] = df_56['text'].apply(get_emotion)
df_57[['label', 'score']] = df_57['text'].apply(get_emotion)

# 6. 결과 저장 (선택사항)
df_56.to_csv("5.6_감정분석결과.csv", index=False, encoding='utf-8-sig')
df_57.to_csv("5.7_감정분석결과.csv", index=False, encoding='utf-8-sig')
