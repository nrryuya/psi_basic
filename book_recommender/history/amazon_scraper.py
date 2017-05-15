from .models import Book
from bs4 import BeautifulSoup
import requests


def get_soup(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    return soup


# 商品ページのurlからname, text, urlを取得
def get_title(url):
    soup = get_soup(url)
    name = soup.select("#productTitle")
    text = soup.select("#productDescription_feature_div")
    amazon_url = url[0:46]
    return name, text, amazon_url


# データベースに保存
def save_book(name, text, amazon_url):
    book, created = Book.objects.get_or_create(amazon_url=amazon_url)
    book.name = name
    book.text = text
    book.save()


# 商品ページのurlリストを作るメソッド
def make_product_urls():
    pass
