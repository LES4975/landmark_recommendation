import pandas as pd
from wordcloud import WordCloud
import collections
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 폰트 불러 오기
font_path = './malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rc('font', family='NanumBarunGothic')

#데이터셋 불러와서 인덱싱
df = pd.read_csv('./dataset/LES/cleaned_reviews/Chungnam_cleaned_reviews.csv')
words = df.iloc[1, 1].split()
print(words)
sentence = df.iloc[1, 1]
print(sentence)
words = sentence.split()

# 단어사전으로 만들기
worddict = collections.Counter(words)
worddict = dict(worddict)
print(worddict)

wordcloud_img = WordCloud(
    background_color='white', max_words=2000, font_path=font_path
    ).generate_from_frequencies(worddict)
plt.figure(figsize=(10, 10))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
plt.show()