import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# 1. CSV 파일 불러오기 (title 열 필요)
df = pd.read_csv('genshin_5.7.csv')

# 2. KoBERT 모델과 토크나이저 불러오기
model_name = "slave-factory/kobert-emotion-classifier-v3"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)
model.eval()

# 3. 감정 분류 레이블 정의
labels = ['기쁨', '당황', '분노', '불안', '슬픔', '상처', '중립']

# 4. 감정 예측 함수 정의
def predict_emotion(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    return labels[predicted_class]

# 5. title 열 기준 감정 분석 실행
df['감정'] = df['title'].astype(str).apply(predict_emotion)

# 6. 결과 저장 (새 CSV로)
df.to_csv('result5.7_with_emotion.csv', index=False)

# 7. 감정별 통계
summary_df = df['감정'].value_counts().reset_index()
summary_df.columns = ['감정', '건수']
summary_df['비율'] = round((summary_df['건수'] / len(df)) * 100, 1).astype(str) + '%'

print(summary_df)
