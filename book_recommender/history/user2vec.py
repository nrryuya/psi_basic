from django.core.cache import cache
import MeCab
import gensim
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from history.np_scraper import login_np, get_picked_articles
from book_recommender.local_settings import MECAB_PATH


# text中の名詞の分散表現の平均のベクトルをだす
def extract_keyword(text):
    """textを形態素解析して、名詞のみのリストを返す"""
    m = MeCab.Tagger(MECAB_PATH)
    m.parse('')
    node = m.parseToNode(text).next
    keywords = []
    while node:
        if node.feature.split(",")[0] == "名詞":
            keywords.append(node.surface)
        node = node.next
    return keywords[:-1]


def text2vec(text):
    # NOTE: vectorize_userの中で呼び出した方が早いのかもしれない
    fastText_model_cache_key = 'fastText_model_cache'
    model = cache.get(fastText_model_cache_key)

    if model is None:
        model = gensim.models.KeyedVectors.load_word2vec_format('history/model.vec', binary=False)
        # save in django memory cache
        cache.set(fastText_model_cache_key, model, None)
        print("loaded model")
    else:
        print("use cashed model")

    separated_text = extract_keyword(text)
    vec = np.zeros(300)
    count = 0
    for word in separated_text:
        try:
            # vec+= model[word] * idf_dict[word]
            vec += model[word]  # NOTE: modelにない単語はinferした方が良いかもしれない
            count += 1
        except:
            continue
    if count == 0:
        return np.zeros(300)
    else:
        return vec / count


# Picked記事のタイトルの分散表現の平均によるユーザーベクトルを作る
def vectorize_user(titles_df):
    titles_df['vectorized_title'] = titles_df['title'].apply(text2vec)
    vector = np.zeros(300)
    count = 0
    for title_vec in titles_df['vectorized_title']:
        vector += title_vec
        count += 1
    vector = vector / count
    return vector.reshape(1, -1)


# NOTE: クラスタリングの実験用。
# Picked記事のタイトルとその分散表現のDataFrameを返す。
def get_title_vectors(user_url):
    driver = login_np()
    driver.get(user_url)  # 過去Pick記事一覧
    titles_df = get_picked_articles(driver)
    titles_df['vectorized_title'] = titles_df['title'].apply(text2vec)
    return titles_df


# NOTE: クラスタリングの実験用。
def make_cosine_sim_matrix(titles_df):  # 記事同士のコサイン類似度の二次元リスト
    matrix = []
    i = 0
    for vector1 in titles_df['vectorized_title']:
        matrix.append([])
        for vector2 in titles_df['vectorized_title']:
            score = cosine_similarity(vector1.reshape(1, -1), vector2.reshape(1, -1))
            matrix[i].append(score)
        i += 1
    return matrix

# 記事のベクトルのリストをクラスタリング
# def clustering_titles(titles_df):
