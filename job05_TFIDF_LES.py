import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread

# 전처리한 데이터셋을 하나로 합친 뒤 TF-IDF 구하기

local_LES = ['Chungbuk', 'Chungnam', 'Daegu', 'Jeonnam', 'Ulsan'] # 지역명
local_PMW = ['Busan', 'Gyeongsangbuk_do', 'Gyeongsangnam_do', 'Jeollabuk_do', 'Seoul']
location = [local_LES, local_PMW]
folders = ['./dataset/LES/cleaned_reviews/', './dataset/PMW/cleaned_reviews/']
NAME = ['LES', 'PMW']
all_reviews = pd.DataFrame(columns=['reviews'])
all_landmark = pd.DataFrame(columns=['names', 'reviews', 'average_rating', 'location'])

for i in range(2):
    folder = folders[i]
    local = location[i]
    print(folder, local)

    df_reviews = pd.DataFrame(columns=['reviews'])
    df_landmark = pd.DataFrame(columns=['names', 'reviews', 'average_rating', 'location'])

    for path in local:
        print(path)
        df = pd.read_csv(folder + path + '_cleaned_reviews.csv')
        df.info()

        df_landmark = pd.concat([df_landmark, df], ignore_index=True)
        df_reviews = pd.concat([df_reviews, df[['reviews']]], ignore_index=True)
        df_reviews.info()
        print(df_reviews.head())

    df_reviews.to_csv(folder + NAME[i] + '_only_reviews.csv', index=False)
    df_landmark.to_csv(folder + NAME[i] + '_All_cleaned_reviews.csv', index=False)

    all_reviews = pd.concat([all_reviews, df_reviews], ignore_index=True)
    all_landmark = pd.concat([all_landmark, df_landmark], ignore_index=True)

# 중복 제거
all_reviews = all_reviews.drop_duplicates()
all_landmark = all_landmark.drop_duplicates(subset='reviews')

all_reviews.to_csv('./dataset/All_only_reviews.csv', index=False)
all_landmark.to_csv('./dataset/All_cleaned_reviews.csv', index=False)

tfidf = TfidfVectorizer(sublinear_tf=True)
tfidf_matrix = tfidf.fit_transform(all_reviews['reviews'])
print(tfidf_matrix.shape)
print(tfidf_matrix[0])

import pickle

with open('./models/reviews_tfidf.pickle', 'wb') as f:
    pickle.dump(tfidf, f)
mmwrite('./models/tfidf_landmark_reviews.mtx', tfidf_matrix)  # 매트릭스로써 저장

