# 필요한 라이브러리 임포트
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import platform
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

#%% 데이터 로드 및 초기 탐색
# CSV 파일 읽기
df_5_6 = pd.read_csv('result5.6_with_emotion.csv')
df_5_7 = pd.read_csv('result5.7_with_emotion.csv')

# 감정별 건수 계산
def calculate_emotion_stats(df):
    # 감정별 건수 계산
    emotion_counts = df['감정'].value_counts()
    
    # 감정별 비율 계산
    emotion_ratios = (df['감정'].value_counts(normalize=True) * 100).round(2)
    )
    
    # 결과를 데이터프레임으로 변환
    result_df = pd.DataFrame({
        '건수': emotion_counts,
        '비율': emotion_ratios.astype(str) + '%'
    })
    
    return result_df

# 각 데이터셋의 감정 통계 계산
stats_5_6 = calculate_emotion_stats(df_5_6)
stats_5_7 = calculate_emotion_stats(df_5_7)

print("=== 5.6 버전 감정 분석 결과 ===")
print("\n감정별 건수 및 비율:")
print(stats_5_6)
print("\n데이터 정보:")
print(df_5_6.info())
print("\n결측치 확인:")
print(df_5_6.isnull().sum())

print("\n=== 5.7 버전 감정 분석 결과 ===")
print("\n감정별 건수 및 비율:")
print(stats_5_7)
print("\n데이터 정보:")
print(df_5_7.info())
print("\n결측치 확인:")
print(df_5_7.isnull().sum())

#%% 비율 데이터 전처리
def convert_percentage_to_float(stats_df):
    # 비율 컬럼에서 % 제거하고 float로 변환
    stats_df['비율_float'] = stats_df['비율'].str.rstrip('%').astype('float') / 100
    )
    return stats_df

# 전처리 적용
stats_5_6_processed = convert_percentage_to_float(stats_5_6.copy())
stats_5_7_processed = convert_percentage_to_float(stats_5_7.copy())

print("\n=== 5.6 버전 전처리된 감정 분석 결과 ===")
print(stats_5_6_processed)

print("\n=== 5.7 버전 전처리된 감정 분석 결과 ===")
print(stats_5_7_processed)

#%% 기본 통계량 출력
print("\n=== 5.6 버전 감정 통계 요약 ===")
print("\n건수 통계:")
print(stats_5_6_processed['건수'].describe())
print("\n비율 통계:")
print(stats_5_6_processed['비율_float'].describe())

print("\n=== 5.7 버전 감정 통계 요약 ===")
print("\n건수 통계:")
print(stats_5_7_processed['건수'].describe())
print("\n비율 통계:")
print(stats_5_7_processed['비율_float'].describe())

#%% 이상치 확인 (IQR 방식)
def check_outliers(stats_df, column):
    Q1 = stats_df[column].quantile(0.25)
    Q3 = stats_df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = stats_df[(stats_df[column] < lower_bound) | (stats_df[column] > upper_bound)][column]
    )
    
    if len(outliers) > 0:
        print(f"\n{column} 컬럼의 이상치:")
        print(f"이상치 개수: {len(outliers)}")
        print(f"이상치 값: {outliers.values}")

print("\n=== 5.6 버전 이상치 확인 ===")
check_outliers(stats_5_6_processed, '건수')
check_outliers(stats_5_6_processed, '비율_float')

print("\n=== 5.7 버전 이상치 확인 ===")
check_outliers(stats_5_7_processed, '건수')
check_outliers(stats_5_7_processed, '비율_float')

#%% 긍정/부정 감정 분류 및 비율 계산
# 감정 분류 정의
emotion_categories = {
    '긍정': ['기쁨', '행복', '즐거움', '희망', '만족'],
    '부정': ['슬픔', '분노', '불안', '상처', '걱정', '우울', '두려움', '불만', '실망']
}

def classify_emotion(emotion):
    """감정을 긍정/부정으로 분류하는 함수"""
    for category, emotions in emotion_categories.items():
        if emotion in emotions:
            return category
    return '기타'  # 분류되지 않은 감정은 '기타'로 처리


def calculate_sentiment_ratio(df):
    """데이터프레임의 감정을 긍정/부정으로 분류하고 비율을 계산하는 함수"""
    # 감정 분류 적용
    df['감정_분류'] = df['감정'].apply(classify_emotion)
    )
    
    # 분류별 건수 계산
    sentiment_counts = df['감정_분류'].value_counts()
    )
    
    # 분류별 비율 계산
    sentiment_ratios = (df['감정_분류'].value_counts(normalize=True) * 100).round(2)
    )
    
    # 결과를 데이터프레임으로 변환
    result_df = pd.DataFrame({
        '건수': sentiment_counts,
        '비율': sentiment_ratios.astype(str) + '%'
    })
    
    return result_df

# 각 버전별 긍정/부정 비율 계산
sentiment_5_6 = calculate_sentiment_ratio(df_5_6)
sentiment_5_7 = calculate_sentiment_ratio(df_5_7)

print("\n=== 5.6 버전 긍정/부정 감정 분석 ===")
print(sentiment_5_6)

print("\n=== 5.7 버전 긍정/부정 감정 분석 ===")
print(sentiment_5_7)

#%% 버전별 긍정/부정 비율 비교 데이터프레임 생성
def create_comparison_df(sentiment_5_6, sentiment_5_7):
    """두 버전의 긍정/부정 비율을 비교하는 데이터프레임 생성"""
    # 비율에서 % 제거하고 float로 변환
    ratio_5_6 = sentiment_5_6['비율'].str.rstrip('%').astype('float') / 100
    )
    ratio_5_7 = sentiment_5_7['비율'].str.rstrip('%').astype('float') / 100
    )
    
    # 비교 데이터프레임 생성
    comparison_df = pd.DataFrame({
        '5.6_건수': sentiment_5_6['건수'],
        '5.6_비율': ratio_5_6,
        '5.7_건수': sentiment_5_7['건수'],
        '5.7_비율': ratio_5_7
    })
    
    # 비율 변화 계산
    comparison_df['비율_변화'] = (comparison_df['5.7_비율'] - comparison_df['5.6_비율']).round(4)
    )
    
    return comparison_df

# 비교 데이터프레임 생성 및 출력
comparison_df = create_comparison_df(sentiment_5_6, sentiment_5_7)

print("\n=== 5.6 vs 5.7 버전 긍정/부정 감정 비교 ===")
print(comparison_df)

#%% 시각화를 위한 데이터 준비
def prepare_visualization_data(sentiment_5_6, sentiment_5_7):
    """시각화를 위한 데이터 준비"""
    # 모든 가능한 감정 분류 가져오기
    all_categories = set(sentiment_5_6.index) | set(sentiment_5_7.index)
    )
    
    # 각 버전의 비율 데이터 준비
    ratio_5_6 = sentiment_5_6['비율'].str.rstrip('%').astype('float') / 100
    )
    ratio_5_7 = sentiment_5_7['비율'].str.rstrip('%').astype('float') / 100
    )
    
    # 모든 카테고리에 대해 데이터프레임 생성
    viz_data = []
    for category in all_categories:
        row = {
            '감정_분류': category,
            '5.6_비율': ratio_5_6.get(category, 0),
            '5.7_비율': ratio_5_7.get(category, 0)
        }
        viz_data.append(row)
    
    return pd.DataFrame(viz_data)

viz_data = prepare_visualization_data(sentiment_5_6, sentiment_5_7)

print("\n=== 시각화용 데이터 ===")
print(viz_data)

#%% 한글 폰트 설정 (시각화용)
# 한글 폰트 설정 함수
if platform.system() == 'Windows':
    font_path = 'C:/Windows/Fonts/malgun.ttf'
    plt.rc('font', family='Malgun Gothic')
else:
    font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  # 예시
    plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

#%% 1. 5.6/5.7 버전 감정 비율 비교 막대그래프
plt.figure(figsize=(8, 6))
bar_width = 0.35
index = np.arange(len(stats_5_6_processed.index))

plt.bar(index - bar_width/2, stats_5_6_processed['비율_float'], bar_width, label='5.6 버전')
plt.bar(index + bar_width/2, stats_5_7_processed['비율_float'].reindex(stats_5_6_processed.index, fill_value=0), bar_width, label='5.7 버전')

plt.xlabel('감정')
plt.ylabel('비율')
plt.title('5.6 vs 5.7 버전 감정 비율 비교')
plt.xticks(index, stats_5_6_processed.index)
plt.legend()
plt.tight_layout()
plt.savefig('emotion_ratio_bar.png')
plt.show()

#%% 2. 긍정/부정 감정 비율 파이차트
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
# 5.6 버전
axes[0].pie(sentiment_5_6['건수'], labels=sentiment_5_6.index, autopct='%1.1f%%', startangle=90, colors=['#6fa8dc', '#e06666'])
axes[0].set_title('5.6 긍정/부정 비율')
# 5.7 버전
axes[1].pie(sentiment_5_7['건수'], labels=sentiment_5_7.index, autopct='%1.1f%%', startangle=90, colors=['#6fa8dc', '#e06666'])
axes[1].set_title('5.7 긍정/부정 비율')
plt.tight_layout()
plt.savefig('sentiment_pie.png')
plt.show()

#%% 2-2. 긍정/부정 감정 비율 막대그래프
plt.figure(figsize=(6, 5))
bar_width = 0.35
sentiments = list(set(sentiment_5_6.index) | set(sentiment_5_7.index))
index = np.arange(len(sentiments))
plt.bar(index - bar_width/2, [sentiment_5_6['비율_float'].get(s, 0) if '비율_float' in sentiment_5_6 else sentiment_5_6['비율'].str.rstrip('%').astype('float').get(s, 0)/100 for s in sentiments], bar_width, label='5.6 버전')
plt.bar(index + bar_width/2, [sentiment_5_7['비율_float'].get(s, 0) if '비율_float' in sentiment_5_7 else sentiment_5_7['비율'].str.rstrip('%').astype('float').get(s, 0)/100 for s in sentiments], bar_width, label='5.7 버전')
plt.xlabel('감정 분류')
plt.ylabel('비율')
plt.title('긍정/부정 감정 비율 비교')
plt.xticks(index, sentiments)
plt.legend()
plt.tight_layout()
plt.savefig('sentiment_bar.png')
plt.show()

#%% 3. 감정별 건수 히트맵 (버전별 분포)
# 버전별 감정 건수 데이터프레임 생성
heatmap_df = pd.DataFrame({
    '5.6': stats_5_6_processed['건수'],
    '5.7': stats_5_7_processed['건수'].reindex(stats_5_6_processed.index, fill_value=0)
})
plt.figure(figsize=(6, 4))
sns.heatmap(heatmap_df, annot=True, fmt='d', cmap='YlGnBu')
plt.title('버전별 감정 건수 히트맵')
plt.ylabel('감정')
plt.xlabel('버전')
plt.tight_layout()
plt.savefig('emotion_heatmap.png')
plt.show()

#%% 4단계. 랜덤포레스트 모델 생성 및 가설 검증
# 1. 데이터 통합 및 전처리
# 감정별 건수 및 비율을 feature로 변환, 버전(5.6=0, 5.7=1) 추가
features_5_6 = stats_5_6_processed[['건수', '비율_float']].copy()
features_5_6.columns = [f'{col}_5_6' for col in features_5_6.columns]
features_5_6['버전'] = 0
# "감정"이 인덱스인 경우, reset_index()를 이용해 "감정"을 컬럼으로 변환
features_5_6 = features_5_6.reset_index().rename(columns={'index': '감정'})

features_5_7 = stats_5_7_processed[['건수', '비율_float']].copy()
features_5_7.columns = [f'{col}_5_7' for col in features_5_7.columns]
features_5_7['버전'] = 1
# "감정"이 인덱스인 경우, reset_index()를 이용해 "감정"을 컬럼으로 변환
features_5_7 = features_5_7.reset_index().rename(columns={'index': '감정'})

# 이후, "감정" 컬럼을 기준으로 병합 (outer join, 결측치는 0으로 대체)
merged = pd.merge(features_5_6, features_5_7, on='감정', how='outer').fillna(0)

# feature와 target 분리
y = merged['버전_x'].astype(int)  # 5.6=0, 5.7=1
X = merged[[col for col in merged.columns if col.startswith('건수') or col.startswith('비율')]]

# 2. train/test 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 3. 랜덤포레스트 분류기 학습 및 예측
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

# 4. 중요 변수(feature importance) 시각화
importances = rf.feature_importances_
feature_names = X.columns

plt.figure(figsize=(8, 5))
plt.barh(feature_names, importances)
plt.xlabel('중요도')
plt.title('랜덤포레스트 Feature Importance')
plt.tight_layout()
plt.savefig('rf_feature_importance.png')
plt.show()

# 5. 모델 성능 평가
print('\n=== 랜덤포레스트 모델 성능 평가 ===')
print('정확도:', accuracy_score(y_test, y_pred))
print('혼동행렬:\n', confusion_matrix(y_test, y_pred))
print('분류 리포트:\n', classification_report(y_test, y_pred)) 