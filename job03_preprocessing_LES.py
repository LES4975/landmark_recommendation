import numpy as np
import pandas as pd
import re
from konlpy.tag import Okt

# 불용어 제거
stop_words = ['이다', '아니다', '그렇다', '하다', '있다',
              '보다', '보고', '없다', '오다'] # 리뷰 판별에 별 도움 안 되는 형태소들(필요할 때마다 추가)

folder = './dataset/LES/google_maps_reviews/' # 데이터셋 저장 경로
local = ['Chungbuk', 'Chungnam', 'Daegu', 'Jeonnam', 'Ulsan'] # 지역명

okt = Okt()

for path in local:
    df = pd.read_csv(folder + path + '_reviews.csv')
    df.dropna(inplace=True)
    df.info()
    print(df.head())

    # 불용어 제거, 형태소로 분리
    cleaned_sentences = []
    for review in df.reviews:
        review = re.sub('[^가-힣]', ' ', review)
        tokened_review = okt.pos(review, stem=True)  # pos는 형태소와 형태소의 품사까지 구분하여 저장할 수 있게 해 준다.
        # print(tokened_review)
        df_token = pd.DataFrame(tokened_review, columns=['word', 'class'])
        df_token = df_token[(df_token['class'] == 'Noun') |
                            (df_token['class'] == 'Adjective') |
                            (df_token['class'] == 'Verb')]  # 필요한 품사만 인덱싱
        # print(df_token)
        words = []
        for word in df_token.word:
            if 1 < len(word):  # 2글자 이상의 형태소만 words에 추가한다
                if word not in stop_words:  # stop_words 이외의 형태소만 words에 추가 - (05/26) 추가
                    words.append(word)
        cleaned_sentence = ' '.join(words)
        print(cleaned_sentence)
        cleaned_sentences.append(cleaned_sentence)
    df['reviews'] = cleaned_sentences # 정제한 문장을 데이터프레임

    # 평점 계산하기
    average_list = []
    for rate in df.rating:
        r = [int(num) for num in rate if num.isdigit()]
        if len(r) == 0:
            average = np.nan
        else:
            average = sum(r) / len(r)
        print(average)
        average_list.append(average)
    df['average_rating'] = average_list # 평점 평균을 데이터프레임에 추가

    df.dropna(inplace=True) # 결측치 제거
    df.drop_duplicates(inplace=True)
    df = df.drop('rating', axis=1)
    df.info()

    df.to_csv('./dataset/LES/cleaned_reviews/' + path + '_cleaned_reviews.csv', index=False)

# 불필요한 장소를 쳐내기 위한 확인용 코드
for path in local:
    df = pd.read_csv('./dataset/LES/cleaned_reviews/' + path + '_cleaned_reviews.csv')
    print("####################")
    print(path)
    for name in df.names:
        print(name)

for path in local:
    df = pd.read_csv('./dataset/LES/cleaned_reviews/' + path + '_cleaned_reviews.csv')
    # 불필요한 장소 데이터 제거
    remove_keywords = ['소녀상', '시청', '문화센터', '휴게소', '문화체육센터',
                       '스타디움', '대구제일교회', '운동장', '캠퍼스', '문화의집',
                       'DGB', '서킷', '경기장', '한복입고', '아카데미']
    for word in remove_keywords:
        df = df[~df['names'].str.contains(word, na=False, case=False)]
    df.info()
    df.to_csv('./dataset/LES/cleaned_reviews/' + path + '_cleaned_reviews.csv', index=False)