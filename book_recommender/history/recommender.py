import pandas as pd
import numpy as np
from history.models import Book
from sklearn.metrics.pairwise import cosine_similarity


# ユーザーのベクトルからおすすめ書籍のリストを返すメソッド
#: {'name': 本の名前, 'rakuten_url': URL, 'rakuten_category': 楽天ブックスのカテゴリ, 'score': スコア}のリストで返される
def recommend(user_vector):
    names = Book.objects.values_list('name', flat=True)
    rakuten_urls = Book.objects.values_list('rakuten_url', flat=True)
    rakuten_categories = Book.objects.values_list('rakuten_url', flat=True)
    vectors = list(map(lambda x: np.array(list(map(float, x.split(',')))),
                       Book.objects.values_list('vector', flat=True)))
    scores = list(map(lambda x: cosine_similarity(x.reshape(1, -1), user_vector), vectors))

    books = []

    for (name, rakuten_url, rakuten_category, score) in zip(names, rakuten_urls, rakuten_categories, scores):
        books.append({'name': name, 'rakuten_url': rakuten_url,
                      'rakuten_category': rakuten_category, 'score': score})

    # 上位10件
    recommend_books = sorted(books, key=lambda x: -x['score'])[0:10]
    return recommended_books


# NOTE: DataFrameを作る場合
# def recommend(user_vector):
    # names_df = pd.DataFrame({'name': Book.objects.values_list('name', flat=True)})
    # rakuten_urls_df = pd.DataFrame(
    #     {'rakuten_url': Book.objects.values_list('rakuten_url', flat=True)})
    # rakuten_categories_df = pd.DataFrame(
    #     {'rakuten_category': Book.objects.values_list('rakuten_category', flat=True)})
    #
    # vector_list = list(map(lambda x: np.array(list(map(float, x.split(',')))),
    #                        Book.objects.values_list('vector', flat=True)))
    # scores_df = pd.DataFrame(
    #     {'score': list(map(lambda x: cosine_similarity(x.reshape(1, -1), user_vector), vector_list))})
    #
    # books_df = pd.concat(
    #     [names_df, rakuten_urls_df, rakuten_categories_df, scores_df], axis=1)
