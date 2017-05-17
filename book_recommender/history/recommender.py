from history.models import Book
from sklearn.metrics.pairwise import cosine_similarity


# 文字列に戻すのは ','.join(li)
def string_to_list(string):
    return string.split(',')


# ユーザーのベクトルからおすすめ書籍のリストを返すメソッド
#: 次のような辞書型で返される。{'name': 本の名前, 'rakuten_url': 楽天ブックスのURL, 'rakuten_category': 楽天ブックスのカテゴリ}
def recommend(user_vector):
    # カテゴリでフィルターするかも
    # books = Book.objects.filter(category=category)
    books = Book.objects.all()

    names_df = pd.DataFrame({'name': Book.objects.values('name')})
    rakuten_urls_df = pd.DataFrame({'rakuten_url': Book.objects.values('rakuten_url')})
    rakuten_categories_df = pd.DataFrame(
        {'rakuten_category': Book.objects.values('rakuten_category')})

    vector_list = map(lambda x: ','.join(x), list(Book.objects.values('vector')))
    scores_df = pd.DataFrame({'score': map(lambda x: x, vector_list)})

    books_df = pd.concat(
        [names_df, rakuten_urls_df, rakuten_categories_df, scores_df], axis=1)
    # score上位10件を取得し、辞書型に変換
    recommended_books = books_df.sort_values(by='score', ascending=False)[0:10].to_dict()

    return recommended_books
