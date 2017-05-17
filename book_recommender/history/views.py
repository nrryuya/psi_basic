from django.shortcuts import render
from readability.readability import Document
import re
from bs4 import BeautifulSoup
import requests
from history.user2vec import vectorize_user
from history.recommender import recommend


# NewsPicksのアカウントURLを受け取っておすすめ書籍のリストを表示するメソッド
# TODO; celeryで非同期処理する
def recommend_books(request):
    url = request.POST['url']
    user_vector = vectorize_user(url)
    # {'name': 本の名前, 'rakuten_url': 楽天ブックスのURL, 'rakuten_category': 楽天ブックスのカテゴリ, 'score': コサイン類似度}という辞書のリストが返される。
    books = recommend(user_vector)
    context = {'books': books}
    return render(request, 'history/result.html', context)


# NewsPicksのアカウントURLをPOSTするページを表示する
def send_account(request):
    return render(request, 'history/send_account.html')


# URLから記事本文を抜き出すメソッド
# NOTE: 使わないかも
# def get_content(url):
#     try:
#         response = requests.get(url)
#         doc = Document(response.text)
#         soup = BeautifulSoup(doc.summary(), 'lxml')
#         content = soup.text
#         pattern = r'　+$|\s+$'
#         repatter = re.compile(pattern)
#         print("try:" + url)
#         if not (content == "" or repatter.match(content)):
#             print("readability worked")
#             print("content: " + content)
#             return content
#         else:
#             print("not worked like: " + content)
#             content = get_body(response)
#             print("content: " + content)
#             return content
#     except:
#         return "error"
