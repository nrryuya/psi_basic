import pandas as pd
import MeCab
import math
import gensim
# import pickle
from np_scraper import get_picked_articles
from book_recommender.local_settings import MECAB_PATH

m = MeCab.Tagger(MECAB_PATH)
model = gensim.models.KeyedVectors.load_word2vec_format('model.vec', binary=False)


# text中の名詞、動詞の分散表現の平均のベクトルをだす
def text2vec(text):
    separated_text = m.parse(text)
    vec = 0
    count = 0
    for word in separated_text:
        try:
            # vec+= model[word] * idf_dict[word]
            vec += model[word]
            count += 1
        except:
            continue
    if count == 0:
        return 0
    else:
        return vec / count


# Picked記事のタイトルの分散表現の平均によるユーザーベクトルを作る
def vectorize_user(user_url):
    titles_df = get_picked_articles(user_url)
    titles_df['vectorized_title'] = titles_df['title'].apply(text2vec)
    vector = 0
    count = 0
    for title_vec in titles_df['vectorized_title']:
        vector += title_vec
        count += 1
    vector = vector / count
    return vector
