import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt

def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1])) # 코사인 유사도 행렬을 enumerate
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True) # 유사도가 제일 큰 것부터 내림차순으로 정렬
    simScore = simScore[:11] # 상위 11개까지 simScore에 저장
    landmark_idx = [i[0] for i in simScore]
    rec_movie_list = df_reviews.iloc[landmark_idx, 0]
    return rec_movie_list[1:11] # 자기 자신(0번째)을 제외하고 1~10번째 장소를 출력

df_reviews = pd.read_csv('./dataset/All_only_reviews.csv')
df_landmarks = pd.read_csv('./dataset/All_cleaned_reviews.csv')
tfidf_matrix = mmread('./models/tfidf_landmark_reviews.mtx').tocsr()
with open('./models/reviews_tfidf.pickle', 'rb') as f:
    tfidf = pickle.load(f)

# 인덱스를 이용한 추천
# ref_idx = 150 # 특정 장소의 인덱스
# print(df_reviews.iloc[ref_idx, 0])
# cosine_sim = linear_kernel(tfidf_matrix[ref_idx], tfidf_matrix) # 특정 장소의 벡터와 모든 장소의 벡터 간의 cosine 값을 구함
# print(cosine_sim) # 코사인 유사도
# print(len(cosine_sim[0])) # 장소 갯수만큼 나온다
# recommendation = getRecommendation(cosine_sim)
# print(recommendation)

# keyword 기반 콘텐츠 추천
from gensim.models import Word2Vec

embedding_model = Word2Vec.load('./models/word2vec_landmark_review.models')
keyword = '여름'
sim_word = embedding_model.wv.most_similar(keyword, topn=10)
words = []
for word, _ in sim_word:
    words.append(word)
sentence = []
count = 10

# 키워드의 유사 단어를 찾아서 문장 구성
for word in words:
    sentence = sentence + [word] * count
    count -= 1
sentence = ' '.join(sentence)
print(sentence)

# tf-idf를 이용해서 장소 추천
sentence_vec = tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation)

# 1) Extract those indices
recommended_indices = recommendation.index.tolist()

# 2) Look up the names in df_landmarks
recommended_places = df_landmarks.loc[recommended_indices, 'names']  # <-- replace 'name' with your actual landmark-name column

print(keyword+" 느낌이 나는 장소를 추천합니다.")
print("추천 장소명:")
print(recommended_places)