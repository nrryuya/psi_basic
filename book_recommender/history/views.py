from django.shortcuts import render
from readability.readability import Document
import re
from bs4 import BeautifulSoup
import requests
from history.np_scraper import vectorize_user
from history.recommender import recommend


# NewsPicksのアカウントURLを受け取っておすすめ書籍のリストを表示するメソッド
def recommend_books(requests):
    url = request.POST['url']
    vector = vectorize_user(url)
    books = recommend(vector)
    # TODO: ここに処理を書き、必要な値をcontenxtに入れて返す
    context = {}
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
