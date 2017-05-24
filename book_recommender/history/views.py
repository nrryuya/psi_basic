from django.shortcuts import render
# from readability.readability import Document
import re
from bs4 import BeautifulSoup
import requests
import numpy as np
from history.np_scraper import login_np, get_username
from history.user2vec import *
from history.recommender import recommend
from history.kmeans import get_cluster


# NewsPicksのアカウントURLを受け取っておすすめ書籍のリストを表示する
# TODO: celeryで非同期処理する
def recommend_books(request):
    url = request.POST['url']
    driver = login_np()
    driver.get(url)  # 過去Pick記事一覧
    username = get_username(driver)
    titles_df = get_title_vectors(driver)
    driver.quit()  # ブラウザを閉じる
    cluster = get_cluster(titles_df)
    print("cluster:")
    print(cluster)
    books = []
    try:
        for c in cluster:
            # {'name': 本の名前, 'rakuten_url': 楽天ブックスのURL, 'rakuten_category': 楽天ブックスのカテゴリ, 'score': コサイン類似度}という辞書のリストが返される。
            books.append(recommend(np.array(c[0])))
        worked = True
    except:  # たまにNaNになる
        books = [[{'name': "本の名前", 'rakuten_url': "http://books.rakuten.co.jp/",
                   'rakuten_category': "楽天ブックスのカテゴリ", 'score': "コサイン類似度"}]]
        worked = False
    context = {'books': books, 'username': username, 'worked': worked}
    return render(request, 'history/recommend_books.html', context)


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
