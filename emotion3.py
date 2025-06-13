import pandas as pd

# 5.6, 5.7 각각 CSV 불러오기
df_56 = pd.read_csv('emotion_56.csv')
df_57 = pd.read_csv('emotion_57.csv')

# 컬럼명 통일, 필요 컬럼만 선택 (ex: emotion_type, count, ratio, version)
df_56 = df_56.rename(columns={'감정종류':'emotion', '건수':'count', '비율':'ratio'})
df_56['version'] = '5.6'

df_57 = df_57.rename(columns={'감정종류':'emotion', '건수':'count', '비율':'ratio'})
df_57['version'] = '5.7'

# 감정 통합 (ex: 긍정, 부정, 중립만 남기기)
positive = ['기쁨', '행복', '감사', '만족'] # 예시
negative = ['분노', '슬픔', '실망', '불만'] # 예시

def emotion_group(e):
    if e in positive:
        return '긍정'
    elif e in negative:
        return '부정'
    else:
        return '중립'

df_56['emotion_group'] = df_56['emotion'].apply(emotion_group)
df_57['emotion_group'] = df_57['emotion'].apply(emotion_group)

# 합치기
df = pd.concat([df_56, df_57], ignore_index=True)

# 이상치 제거(필요시)
df = df[df['count'] > 0]

# CSV로 저장 (필요시)
df.to_csv('emotion_clean.csv', index=False)
