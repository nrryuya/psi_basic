from history.models import Book
from bs4 import BeautifulSoup
import requests
from selenium import webdriver


def get_soup(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    return soup


# 全体。rakutenの各カテゴリーの上位の本のデータをデータベースに保存する。
def make_book_database():
    #############
    # user agent
    user_agent = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36'
    # PhantomJS本体のパス
    pjs_path = '/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs'
    dcap = {
        "phantomjs.page.settings.userAgent": user_agent,
        'marionette': True
    }
    driver = webdriver.PhantomJS(executable_path=pjs_path, desired_capabilities=dcap)

    category_urls = get_category_urls()
    for category_url in category_urls:
        rakuten_category = category_url[0]
        print("start category：")
        print(category_url)
        product_urls = urls_for_each_category(category_url[1], driver)
        for product_url in product_urls:
            print("try：" + product_url)
            name, text, rakuten_url, scraped = get_info(product_url)
            if scraped:
                created = save_book(name, text, rakuten_url, rakuten_category)
                if created:
                    print("saved：")
                else:
                    print("already exists：")
                print([name, text, rakuten_url, rakuten_category])
    driver.quit()


def get_category_urls():
    soup = get_soup('http://books.rakuten.co.jp/ranking/weekly/001/#!/1/')
    category_urls = []
    for item in soup.select("#side-navi a")[1:19]:
        rakuten_category = item.text
        category_url = "http://books.rakuten.co.jp" + item.get("href")
        category_urls.append([rakuten_category, category_url])
    return category_urls


def urls_for_each_category(category_url, driver):
    product_urls = []
    url = category_url + "/0/100/"

    # NOTE: 検索結果2ページ目からtxt-ellipsisがなくなる
    # for i in range(1, 4):
    #     url = category_url[0:-1] + str(i)
    #     print(url)
    #     driver.get(url)
    #     for item in driver.find_elements_by_class_name("txt-ellipsis"):
    #         product_urls.append(item.get_attribute("href"))

    print(url)
    driver.get(url)
    for item in driver.find_elements_by_class_name("txt-ellipsis"):
        product_urls.append(item.get_attribute("href"))

    return product_urls


# 商品ページのurlからname, text, urlを取得
def get_info(url):
    soup = get_soup(url)
    try:
        name = soup.find("h1").text
        text = soup.select(".saleDesc")[0].text
        scraped = True
    except:
        name = None
        text = None
        print("can't get infomation of：")
        print(url)
        scraped = False
    rakuten_url = url
    return [name, text, rakuten_url, scraped]


# データベースに保存
def save_book(name, text, rakuten_url, rakuten_category):
    book, created = Book.objects.get_or_create(rakuten_url=rakuten_url)
    book.name = name
    book.text = text
    book.rakuten_category = rakuten_category
    book.save()
    return created


make_book_database()
