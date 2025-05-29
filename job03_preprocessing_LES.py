import numpy as np
import pandas as pd
import re
from konlpy.tag import Okt

# 불용어 제거
stop_words = ['이다', '아니다', '그렇다', '하다', '있다',
              '보다', '보고', '없다', '오다', '같은', '같다',
              '않다', '되다', '되어다', '야하다', '그냥', '정말',
              '진짜', '너무', '아주', '매우', '완전', '리뷰', '후기'
              '생각', '느낌', '지도', '방문', '여행', '살다', '안되다',
              '가보다', '가다', '들다', '드리다', '싶다', '한번']
# 리뷰 판별에 별 도움 안 되는 형태소들(필요할 때마다 추가)

local_LES = ['Chungbuk', 'Chungnam', 'Daegu', 'Jeonnam', 'Ulsan'] # 지역명
local_PMW = ['Busan', 'Gyeongsangbuk_do', 'Gyeongsangnam_do', 'Jeollabuk_do', 'Seoul']
location = [local_LES, local_PMW] # 지역명 리스트의 리스트
folders = ['./dataset/LES/cleaned_reviews/', './dataset/PMW/cleaned_reviews/'] # 데이터셋 저장 경로
google_maps_folder = ['./dataset/LES/google_maps_reviews/', './dataset/PMW/google_maps_reviews/'] # 데이터셋 저장 경로
okt = Okt()

for i in range(2):
    folder = folders[i]
    local = location[i]

    for path in local:
        df = pd.read_csv(google_maps_folder[i] + path + '_reviews.csv')
        df.dropna(inplace=True)
        df.info()
        print(df.head())
        if df.columns[0] == 'name':  # 컬럼명이 다른지 확인: 'rating'? 'ratings'?
            df.rename(columns={'name': 'names'}, inplace=True)
        if df.columns[2] == 'rating':  # 컬럼명이 다른지 확인: 'rating'? 'ratings'?
            df.rename(columns={'rating': 'ratings'}, inplace=True)

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
        df['reviews'] = cleaned_sentences  # 정제한 문장을 데이터프레임

        # 평점 계산하기
        average_list = []
        for rate in df.ratings:
            r = [int(num) for num in rate if num.isdigit()]
            if len(r) == 0:
                average = np.nan
            else:
                average = sum(r) / len(r)
            print(average)
            average_list.append(average)
        df['average_rating'] = average_list  # 평점 평균을 데이터프레임에 추가

        df.dropna(inplace=True)  # 결측치 제거
        df.drop_duplicates(inplace=True)
        df = df.drop('ratings', axis=1)
        df.info()

        df.to_csv(folder + path + '_cleaned_reviews.csv', index=False)

    # 불필요한 장소를 쳐내기 위한 확인용 코드
    for path in local:
        df = pd.read_csv(folder + path + '_cleaned_reviews.csv')
        print("####################")
        print(path)
        for name in df.names:
            print(name)

    # 불필요한 장소 데이터 제거
    remove_keywords = ['소녀상', '시청', '문화센터', '휴게소', '문화체육센터',
                               '스타디움', '대구제일교회', '운동장', '캠퍼스', '문화의집',
                               'DGB', '서킷', '경기장', '한복입고', '아카데미',
                               "F1963",
                               "부산 아시아드 주 경기장",
                               "Busan Station",
                               "Foot Massage Five Toe",
                               "Seungbu Station",
                               "Korea Institute of Robotics & Technology Convergence",
                               "과학교육원",
                               "합천문화원",
                               "Changwon Football Center",
                               "Changwon Velodrome",
                               "Gunsan Saemangeum Convention Center",
                               "평화의소녀상",
                               "고척스카이돔",
                               "국회 의사당",
                               "코엑스",
                               "올림픽테니스장",
                               "서울특별시 교육연구정보원",
                               "주한중국문화원",
                               "딥띵커",
                               "강서구민회관",
                               "씨제이 이앤엠센터",
                               "광나루 안전체험관",
                               "Mnet Studios",
                               'nowHere',
                               "Minsu Seol",
                               "서울영어과학교육센터",
                               "시즌오브유 퍼스널컬러",
                               "목동청소년센터",
                               "Vog Hair",
                               "The Chapel At Cheongdam"
                               ]
    for path in local:
        df = pd.read_csv(folder + path + '_cleaned_reviews.csv')
        for word in remove_keywords:
            df = df[~df['names'].str.contains(word, na=False, case=False)]
        df.info()
        df.to_csv(folder + path + '_cleaned_reviews.csv', index=False)

    # 중복 제거하고 혹시 몰라서 '지역' column 추가해 두기
    for path in local:
        df = pd.read_csv(folder + path + '_cleaned_reviews.csv')
        df.dropna(inplace=True)
        df['location'] = path
        df.info()
        print(df.head())
        df.to_csv(folder + path + '_cleaned_reviews.csv', index=False)


