from history.models import Book
from bs4 import BeautifulSoup
import requests
from selenium import webdriver


def get_soup(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    return soup


# 全体。Amazonの各カテゴリーの上位の本のデータをデータベースに保存する。
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
        amazon_category = category_url[0]
        print("start category：")
        print(category_url)
        product_urls = urls_for_each_category(category_url[1])
        for product_url in product_urls:
            print("try：" + product_url)
            name, text, amazon_url, scraped = get_info(product_url, driver)
            if scraped:
                save_book(name, text, amazon_url, amazon_category)
                print("saved：")
                print([name, text, amazon_url, amazon_category])

    driver.quit()


def get_category_urls():
    soup = get_soup('https://www.amazon.co.jp/gp/bestsellers/books/')
    category_urls = []
    for item in soup.select("#zg_browseRoot ul a"):
        amazon_category = item.text
        category_url = item.get("href")
        category_urls.append([amazon_category, category_url])
    return category_urls


def urls_for_each_category(category_url):
    product_urls = []
    url = category_url
    # NOTE: 各カテゴリ1ページ目まで取得、それ以降を取得するには下記のような方法ではなく、selenium使った方が良い。
    # for i in range(1,2):
    #     url = category_url + "/#" + str(i)
    #     print(url)
    #     soup = get_soup(url)
    #     for item in soup.select(".a-link-normal"):
    #         if item.find(class_="p13n-sc-truncate p13n-sc-truncated-hyphen p13n-sc-line-clamp-2"):
    #             product_urls.append("https://www.amazon.co.jp" + item.get("href"))
    soup = get_soup(url)
    for item in soup.select(".a-link-normal"):
        if item.find(class_="p13n-sc-truncate p13n-sc-truncated-hyphen p13n-sc-line-clamp-2"):
            product_urls.append("https://www.amazon.co.jp" + item.get("href"))

    return product_urls


# 商品ページのurlからname, text, urlを取得
def get_info(url, driver):
    driver.get(url)
    data = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    # try:
    #     name = soup.select("#productTitle")[0]
    # except:
    #     name = soup.select("#ebooksProductTitle")[0]
    # name = soup.select("#title")[0].text
    try:
        name = soup.find(id="title").text
        text = soup.select("#productDescription")[0].find("p").text
        scraped = True
    except:
        name = None
        text = None
        print("can't get description of：")
        print(url)
        scraped = False
    index = url.find('ref=')
    amazon_url = url[0:index]
    return [name, text, amazon_url, scraped]


# データベースに保存
def save_book(name, text, amazon_url, amazon_category):
    book, created = Book.objects.get_or_create(amazon_url=amazon_url)
    book.name = name
    book.text = text
    book.amazon_category = amazon_category
    book.save()


make_book_database()
