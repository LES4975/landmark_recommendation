import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread

folder = './dataset/LES/cleaned_reviews/' # 데이터셋 저장 경로
local = ['Chungbuk', 'Chungnam', 'Daegu', 'Jeonnam', 'Ulsan'] # 지역명

df_reviews = pd.DataFrame(columns=['reviews'])

for path in local:
    df = pd.read_csv(folder + path + '_cleaned_reviews.csv')
    df.info()

    df_reviews = pd.concat([df_reviews, df[['reviews']]], ignore_index=True)
    df_reviews.info()
    print(df_reviews.head())

    df_reviews.to_csv('./dataset/LES/cleaned_reviews/only_reviews.csv', index=False)

tfidf = TfidfVectorizer(sublinear_tf=True)
tfidf_matrix = tfidf.fit_transform(df_reviews['reviews'])
print(tfidf_matrix.shape)
print(tfidf_matrix[0])

import pickle

with open('./models/reviews_tfidf.pickle', 'wb') as f:
    pickle.dump(tfidf, f)
mmwrite('./models/tfidf_landmark_reviews.mtx', tfidf_matrix)  # 매트릭스로써 저장

