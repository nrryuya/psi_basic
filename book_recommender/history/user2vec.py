import MeCab
import gensim
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from history.np_scraper import get_picked_articles
from book_recommender.local_settings import MECAB_PATH

# TODO: 毎回ロードすると遅い気がする。Djangoサーバーが起動している間常に変数を保持できないのか。
m = MeCab.Tagger(MECAB_PATH)
m.parse('')
model = gensim.models.KeyedVectors.load_word2vec_format('history/model.vec', binary=False)


# text中の名詞の分散表現の平均のベクトルをだす
def extract_keyword(text):
    """textを形態素解析して、名詞のみのリストを返す"""
    node = m.parseToNode(text).next
    keywords = []
    while node:
        if node.feature.split(",")[0] == "名詞":
            keywords.append(node.surface)
        node = node.next
    return keywords[:-1]


def text2vec(text):
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
def vectorize_user(user_url):
    titles_df = get_picked_articles(user_url)
    titles_df['vectorized_title'] = titles_df['title'].apply(text2vec)
    vector = np.zeros(300)
    count = 0
    for title_vec in titles_df['vectorized_title']:
        vector += title_vec
        count += 1
    vector = vector / count
    return vector.reshape(1, -1)


# Picked記事のタイトルとその分散表現のDataFrameを返す。クラスタリングの実験用。
def get_title_vectors(user_url):
    titles_df = get_picked_articles(user_url)
    titles_df['vectorized_title'] = titles_df['title'].apply(text2vec)
    return titles_df


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
