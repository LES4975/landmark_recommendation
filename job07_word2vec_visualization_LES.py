import pandas as pd
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
from matplotlib import font_manager, rc
import matplotlib as mpl

# 폰트 설정
font_path = './malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
mpl.rcParams['axes.unicode_minus'] = False
rc('font', family=font_name)

# 임베딩 모델로 key_word과 유사한 단어 찾기
embedding_model = Word2Vec.load('./models/word2vec_landmark_review.models')
key_word = ('추천')
sim_word = embedding_model.wv.most_similar(key_word, topn=10) # 공간적으로 가까이 있는 단어 찾기
print(sim_word)

# 유사 단어들의 벡터와 단어 이름 추출
vectors = []
labels = []
for label, _ in sim_word:
    labels.append(label)
    vectors.append(embedding_model.wv[label])
print(labels[0])      # 첫 번째 단어
print(vectors[0])     # 첫 번째 단어 벡터
print(len(vectors[0]))  # 벡터 차원 수

df_vectors = pd.DataFrame(vectors)
print(df_vectors.head())

# TSNE로 2차원 축소 (시각화를 위한)
tsne_model = TSNE(perplexity=9, n_components=2, init='pca', n_iter=2500) # 차원 축소 알고리즘, 2차원으로 줄임
new_value = tsne_model.fit_transform(df_vectors)
# 단어, x좌표, y좌표를 담은 DataFrame 생성
df_xy = pd.DataFrame({'words': labels, 'x': new_value[:, 0],
                      'y':new_value[:, 1]})
df_xy.loc[df_xy.shape[0]] = (key_word, 0, 0) # keyword를 (0, 0)에 추가
print(df_xy)
print(df_xy.shape)

# 시각화
plt.figure(figsize=(8, 8))
plt.scatter(0, 0, s=1500, marker='*') # 중심 단어는 별표로 강조
# 각 단어를 중심 단어와 선으로 연결하고 라벨 표시
for i in range(len(df_xy)):
    a = df_xy.loc[[i, 10]] # i번째 단어와 중심 단어
    plt.plot(a.x, a.y, '-D', linewidth=1)
    plt.annotate(df_xy.words[i], xytext=(1, 1), xy=(df_xy.x[i], df_xy.y[i]),
                    textcoords='offset points', ha='right', va='bottom')
plt.show()