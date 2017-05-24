# from django.core.cache import cache
import pandas as pd
from bs4 import BeautifulSoup
# import requests
import time
from selenium import webdriver
from book_recommender.local_settings import NEWSPICKS_ID, NEWSPICKS_PW
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec


# NewsPicksにログインするまで
def login_np():
    # TODO: webdriverをcacheする
    # driver_cache_key = 'driver_cache'
    # driver = cache.get(driver_cache_key)
    #
    # if driver is None:
    #     id = NEWSPICKS_ID
    # （以下略）
        # save in django memory cache
    #     cache.set(driver_cache_key, driver, None)
    #     print("loaded driver")
    #
    # else:
    #     print("use cashed driver")

    id = NEWSPICKS_ID
    pw = NEWSPICKS_PW
    login_url = 'https://newspicks.com'
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
    print("opened login url")
    driver.execute_script(
        "document.querySelector('.register-or-login-items div.login').click();")  # ログインのモーダルだす
    driver.save_screenshot('login-modal.png')
    print("opend login modal")
    # idとpassの入力
    loginid = driver.find_element_by_id('login-username')
    password = driver.find_element_by_id('login-password')
    loginid.clear()
    password.clear()
    loginid.send_keys(id)
    password.send_keys(pw)
    driver.save_screenshot('written-form.png')
    driver.find_element_by_class_name('login-btn').click()  # ログインボタン押下
    # NOTE: time.sleepだけじゃなく、ログインできているか確認して進むようにしても良いかもしれない。
    time.sleep(3.0)
    driver.save_screenshot('clicked-login-btn.png')
    print("logined")

    return driver


def get_username(driver):
    username = driver.find_element_by_class_name('username').text
    return username


def get_picked_articles(driver):
    SCROLL_PAUSE_TIME = 5.0
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    print(last_height)

    for i in range(5):  # 5回までスクロールする
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

    soup = BeautifulSoup(data, "lxml")
    title_list = soup.select(".title")
    titles = []
    for t in title_list:
        titles.append(t.text)

    titles_df = pd.DataFrame({'title': titles[1:-8]})
    return titles_df
