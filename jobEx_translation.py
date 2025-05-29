import pandas as pd
import re
from googletrans import Translator

translator = Translator()

# 영어 문자열만 판별하는 함수
def is_english_only(text):
    return bool(re.fullmatch(r'[A-Za-z\s]+', str(text)))

paths = ['./dataset/LES/cleaned_reviews/LES', './dataset/PMW/cleaned_reviews/PMW', './dataset/KMJ/cleaned_reviews/KMJ']

for i in range(3):
    df = pd.read_csv(paths[i] + '_All_cleaned_reviews.csv')
    df.info()
    print(df.head())

    # 번역 대상만 번역
    translated_names = []
    for name in df['names']:
        if is_english_only(name):
            try:
                translated = translator.translate(name, src='en', dest='ko').text
                translated_names.append(translated)
            except Exception as e:
                print(f"번역 실패: {name} → {e}")
                translated_names.append(name)  # 번역 실패 시 원래 텍스트 유지
        else:
            translated_names.append(name)

    # 결과 덮어쓰기
    df['names'] = translated_names

    # 수정된 결과 저장
    df.to_csv(paths[i] + '_All_cleaned_reviews.csv', index=False, encoding='utf-8-sig')
