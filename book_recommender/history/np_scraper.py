import pandas as pd
from bs4 import BeautifulSoup
# import requests
import time
from selenium import webdriver
from local_settings import NEWSPICKS_ID, NEWSPICKS_PW
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec

id = NEWSPICKS_ID
pw = NEWSPICKS_PW
login_url = 'https://newspicks.com'
SCROLL_PAUSE_TIME = 5.0


def login_np():
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

    driver.get(login_url)  # ログインページを開く
    driver.execute_script(
        "document.querySelector('.register-or-login-items div.login').click();")  # ログインのモーダルだす
    driver.save_screenshot('login-modal.png')

    # idとpassの入力
    loginid = driver.find_element_by_id('login-username')
    password = driver.find_element_by_id('login-password')
    loginid.clear()
    password.clear()
    loginid.send_keys(id)
    password.send_keys(pw)
    driver.save_screenshot('written-form.png')

    driver.find_element_by_class_name('login-btn').click()  # ログインボタン押下
    driver.save_screenshot('clicked-login-btn.png')
    print("logined")
    return driver


def get_picked_articles(user_url):
    driver = login_np()
    driver.get(user_url)  # 過去Pick記事一覧

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    print(last_height)

    for i in range(16):  # 15回までスクロールする
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(new_height)
        if new_height == last_height:
            break
        last_height = new_height

    data = driver.page_source.encode('utf-8')
    driver.quit()  # ブラウザを閉じる

    soup = BeautifulSoup(data, "lxml")
    title_list = soup.select(".title")
    titles = []
    for t in title_list:
        titles.append(t.text)

    titles_df = pd.DataFrame({'title': titles[1:-8]})
    return titles_df
