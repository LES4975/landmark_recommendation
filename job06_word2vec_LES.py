from gensim.models import Word2Vec
import pandas as pd

df_review = pd.read_csv('./dataset/All_only_reviews.csv')
df_review.info()

# 리뷰를 가져 오기!
reviews = list(df_review['reviews'])
print(df_review.iloc[0, 0], reviews[0])

# 리뷰를 나눠서 토큰화
tokens = []
for sentence in reviews:
    token = sentence.split() # 형태소 리스트
    tokens.append(token) # 형태소의 리스트의 리스트
print(tokens[0:2])

# 의미 학습!
embedding_model = Word2Vec(tokens, vector_size=100, window=4,
                           min_count=20, workers=4, epochs=100, sg=1)
# 차원의 저주를 방지하기 위하여 100차원으로 축소, 문맥 window 크기 4, 최소 20회 정도 등장하는 형태소에 대해서만 학습, 학습 시 사용할 코어는 4개, 100회 반복, 학습시킬 때 사용할 알고리즘은 1번
embedding_model.save('./models/word2vec_landmark_review.models') # 모델 저장
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))