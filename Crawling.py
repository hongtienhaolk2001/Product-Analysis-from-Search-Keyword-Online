from function import get_url_com, get_url_time, get_list, convert, clean_comment
from googlesearch import search
import re
from datetime import datetime, date, timedelta
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager


def crawling_data_voz(words_search) -> str:
    '''
    (1)
    Search từ khóa và lấy url từ trang diễn đàn Voz
    Lấy thread chủ đề lưu vào base để xử lý
    '''
    gg = []
    base = []
    query = 'vozforum ' + words_search
    gg = search(query, stop=5)
    for url in gg:
        if (url[0:21] == 'https://vozforum.org/'):
            url = url.split('page-')[0]
            base.append(url)
    '''
    (2)
    Lấy comment và date lưu ở định dạng dataframe
    '''
    comments_full = []
    times_full = []
    for url in base:
        # lấy tất cả comment của tất cả page của mỗi thread
        comments_full.append(get_url_com(url))
        # lấy tất cả time comment của tất cả page của mỗi thread
        times_full.append(get_url_time(url))
    list_com = get_list(comments_full)
    list_time = get_list(times_full)
    data = pd.DataFrame({'time': list_time, 'comment': list_com})

    '''
    (3)
    Clean dữ liệu
    '''
    convert(data)
    data.comment = data.comment.apply(clean_comment)
    data = data.drop_duplicates(subset='comment', keep='first').reset_index()
    data = data.drop(columns='index')
    comt = []
    for i in data.comment:
        if 'You must be registered for see images' in i:
            i = i.replace('You must be registered for see images', '')
        if 'You must be registered for see links' in i:
            i = i.replace('You must be registered for see links', '')
        if 'You must be registered for see medias' in i:
            i = i.replace('You must be registered for see medias', '')
        if 'Được gửi từ' in i:
            i = i.replace('Được gửi từ', '')
        else:
            pass
        i = re.sub(r'\w*for', '', i)
        comt.append(i)
    return data

# def crawling_data_shopee(input_val):


def crawling_data_voz(input_val):
    '''
    '''
    # def find_number(text):
    #     if text == '':
    #         kq = 0
    #     else:
    #         text = text.split()
    #         kq = text[2]
    #         if "k" in kq:
    #             kq = kq.replace('k', '000')
    #             kq = kq.replace(',', '')
    #     kq = int(kq)
    #     return kq

    def collect_search_page(search_url_dict, pages_per_category) -> list:
        '''
        '''
        browser = webdriver.Chrome(
            executable_path='chromedriver.exe')  # Mở trình duyệt web
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        # list_sum = []
        # list_sl = []
        list_link = []
        for i in range(pages_per_category):
            browser.get(search_url_dict)
            time.sleep(5)
            total_height = int(browser.execute_script(
                "return document.body.scrollHeight"))

            for i in range(1, total_height, 100):
                browser.execute_script("window.scrollTo(0, {});".format(i))

            items = browser.find_elements_by_class_name(
                "shopee-search-item-result__item")
            for it in (items):
                urls = it.find_elements_by_css_selector('a')
                for url in urls:
                    url = url.get_attribute("href")
                    list_link.append(url)
                    print(url)

        return list_link

    def search_keyword() -> str:
        search = input_val
        search = search.strip()
        search = search.lower()
        search = search.replace(" ", "%20")
        search_url_dict = 'https://shopee.vn/search?keyword=' + str(search)
        return search_url_dict

    list_link = collect_search_page(search_keyword(), pages_per_category=1)

    def load_url_selenium_shopee(url):
        browser = webdriver.Chrome(
            executable_path='chromedriver.exe')
        print("Loading url=", url)
        browser.get(url)

        list_sum = []
        x = 0
        try:
            while x < 30:
                try:
                    time.sleep(4)
                    total_height = int(browser.execute_script(
                        "return document.body.scrollHeight"))

                    for i in range(0, total_height, 100):
                        browser.execute_script(
                            "window.scrollTo(0, {});".format(i))

                    WebDriverWait(browser, 5).until(
                        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.shopee-product-rating")))

                except:
                    print('No has comment')
                    break

                product_reviews = browser.find_elements_by_css_selector(
                    "[class='shopee-product-rating']")
                # Get product review
                for product in product_reviews:
                    list_per_comment = []
                    # review = product.find_element_by_css_selector("[class='shopee-product-rating__content']").text
                    review = product.find_element_by_css_selector(
                        "[class='_3NrdYc']").text
                    day = product.find_element_by_css_selector(
                        "[class='shopee-product-rating__time']").text
                    day = day.split()
                    day = day[0]
                    if (review != "" or review.strip()):
                        print(review, "/n")
                        # list_review.append(review)
                        # list_time.append(day)
                        list_per_comment.append(day)
                        list_per_comment.append(review)
                        list_per_comment.append('shopee')
                        list_sum.append(list_per_comment)
                # Check for button next-pagination-item have disable attribute then jump from loop else click on the next button

                if len(browser.find_elements_by_css_selector(
                        "button.shopee-icon-button.shopee-icon-button--right[disabled]")) > 0:
                    break
                else:
                    button_next = WebDriverWait(browser, 5).until(EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "button.shopee-icon-button.shopee-icon-button--right")))
                    # driver.execute_script("arguments[0].click();", button_next)
                    button_next.click()
                    print("next page")
                    time.sleep(2)
                    x += 1

        except NoSuchElementException:
            browser.close()

        # list_sum=list(zip(list_time,list_review))
        # list_sum.append(list_per_comment)
        return list_sum

    '''
    Lấy cmt top 30 sản phẩm bán nhiều nhất
    '''

    data_shopee_top30 = []
    # temp=[]
    for i in range(30):
        data_shopee_top30.append(load_url_selenium_shopee(url=list_link[i]))
    # data_shopee.append(temp)
    print("XONG RỒI ĐÓ NHA!!!!!!!!!!!!!!!!!!")

    list_shopee = []
    for i in range(len(data_shopee_top30)):
        df = pd.DataFrame(data_shopee_top30[i], columns=[
                          'time', 'comment', 'Source'])
        list_shopee.append(df)
    # df_shopee.head()
    df_shopee = pd.concat(list_shopee, axis=0, ignore_index=True)

    def time_convert(data):
        for index, i in enumerate(data.time.astype(str)):
            date = datetime.strptime(i.strip(), '%Y-%m-%d')
            data.time[index] = date

    time_convert(df_shopee)

    len(df_shopee)

    return df_shopee


def crawling_data_tiki(text):
    def convert_text_to_string(text):
        '''
        transform text day to datetime format
        '''
        text = text.split()
        x = 1
        if text[4] == 'ngày':
            x = 1
        elif text[4] == 'tháng':
            x = 30
        else:
            x = 365
        today = date.today()

        day = today + timedelta(days=-x * int(text[3]))
        day = day.strftime("%Y/%m/%d")
        day = day.replace('/', '-')
        return day

    def search_keyword_tiki(text):
        '''
        transform url to search
        '''
        input_val = text
        search = input_val
        search = search.strip()
        search = search.lower()
        search = search.replace(" ", "%20")
        # for i in len(search):
        search_url_dict = 'https://tiki.vn/search?q=' + str(search)
        return search_url_dict

    def crawl_list_tiki(url) -> list:
        '''

        '''
        driver = webdriver.Chrome(ChromeDriverManager().install())
        links = []
        driver.get(url)
        # Đoạn scrip để scroll trang web
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(10)
        elem = driver.find_elements_by_xpath("//a[@class='product-item']")
        lt = []
        lt = [el for el in elem]
        for l in lt:
            links.append(l.get_attribute('href'))
        return links

    data_link = crawl_list_tiki(search_keyword_tiki(text))

    def load_url_selenium_tiki(url):
        '''
        '''
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        browser = webdriver.Chrome(executable_path = 'chromedriver.exe')
        browser.get(url)
        list_review = []
        # just craw 10 page
        x = 0
        try:
            while x < 10:
                try:
                    time.sleep(random.randint(1, 3))
                    # auto scroll den 3000px
                    browser.execute_script("window.scrollTo(0, 3000);")
                    browser.execute_script(
                        "window.scrollTo(3000, 5000);")  # từ 3000-5000px vì tiki k thể 1 lần cuộn xuống 5000
                    # Get the review details here
                    WebDriverWait(browser, 10).until(
                        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.review-comment")))
                except:
                    print('Not has comment!')
                    break
                for i in range(3, 8):  # Do các cmt nằm trong xpath từ 3-7 nên trỏ từ 3-8
                    # product_reviews = driver.find_elements_by_xpath("/html/body/div[1]/div[1]/main/div[3]/div[4]/div/div[2]/div["+str(i)+"]")
                    product_reviews = browser.find_elements(By.XPATH,
                                                           "/html/body/div[1]/div[1]/main/div[3]/div[4]/div/div[2]/div[" + str(
                                                               i) + "]")
                    list_comment = []
                    # Get product review
                    for product in product_reviews:
                        review = product.find_element_by_css_selector(
                            "[class='review-comment__content']").text
                        # review = product.find_elements(By.CSS_SELECTOR,"[class='review-comment__content']").text
                        day = browser.find_element_by_xpath(
                            '//*[@id="__next"]/div[1]/main/div[3]/div[4]/div/div[2]/div[3]/div[2]/div[5]/span[1]').text
                        day = convert_text_to_string(day)
                        # day = product.find_element(By.XPATH, "'/html/body/div[1]/div[1]/main/div[3]/div[5]/div/div[2]/div[3]/div[2]/div[5]/span[1]'").text
                        # day = product.find_elements(By.TAG_NAME,"span")
                        # day = set_time(text_day)
                        if (review != "" or review.strip()):
                            # print(review, "\n")
                            list_comment.append(day)
                            list_comment.append(review)
                            print(review)
                            list_comment.append('Tiki')
                            list_review.append(list_comment)
                # Check for button next-pagination-item have disable attribute then jump from loop else click on the next button
                try:
                    button_next = WebDriverWait(browser, 20).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "[class = 'btn next']")))
                    browser.execute_script("arguments[0].click();", button_next)
                    # print("next page " + str(x+1))
                    time.sleep(random.randint(3, 5))
                    x += 1
                except (TimeoutException, WebDriverException) as e:
                    # print('Load several page!')
                    break
        except NoSuchElementException:
            browser.close()
        return list_review

    data_tiki = []
    # temp=[]
    for i in range(len(data_link)):
        data_tiki.append(load_url_selenium_tiki(url=data_link[i]))
        # print('XONG SAN PHAM THU '+ str(i+1))
        # data_tiki.append(temp)
    # print (data_tiki)
    list_tiki = []
    for i in range(len(data_tiki)):
        # df = pd.DataFrame(data_tiki[i],columns=['comment'])
        df = pd.DataFrame(data_tiki[i], columns=['time', 'comment', 'Source'])
        list_tiki.append(df)
        # df_tiki.head()
    df_tiki = pd.concat(list_tiki, axis=0, ignore_index=True)
    return df_tiki


def crawling_data_shopee(input_val):
    # def find_number(text):
    #     if text == '':
    #         kq = 0
    #     else:
    #         text = text.split()
    #         kq = text[2]
    #         if "k" in kq:
    #             kq = kq.replace('k', '000')
    #             kq = kq.replace(',', '')
    #     kq = int(kq)
    #     return kq

    def collect_search_page(search_url_dict, pages_per_category):
        browser = webdriver.Chrome(executable_path='chromedriver.exe')
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        # list_sum = []
        # list_sl = []
        list_link = []

        for i in range(pages_per_category):
            browser.get(search_url_dict)
            time.sleep(5)
            total_height = int(browser.execute_script(
                "return document.body.scrollHeight"))

            for i in range(1, total_height, 100):
                browser.execute_script("window.scrollTo(0, {});".format(i))

            items = browser.find_elements_by_class_name(
                "shopee-search-item-result__item")

            for it in (items):
                urls = it.find_elements_by_css_selector('a')
                for url in urls:
                    url = url.get_attribute("href")
                    list_link.append(url)
                    print(url)

        return list_link

    def search_keyword():
        search = input_val
        search = search.strip()
        search = search.lower()
        search = search.replace(" ", "%20")
        search_url_dict = 'https://shopee.vn/search?keyword=' + str(search)
        return search_url_dict

    # In[5]:

    list_link = collect_search_page(search_keyword(), pages_per_category=1)

    def load_url_selenium_shopee(url):
        browser = webdriver.Chrome(executable_path='chromedriver.exe')
        print("Loading url=", url)
        browser.get(url)

        list_sum = []
        x = 0
        try:
            while x < 30:
                try:
                    time.sleep(4)
                    total_height = int(browser.execute_script(
                        "return document.body.scrollHeight"))

                    for i in range(0, total_height, 100):
                        browser.execute_script(
                            "window.scrollTo(0, {});".format(i))

                    WebDriverWait(browser, 5).until(
                        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.shopee-product-rating")))

                except:
                    print('No has comment')
                    break

                product_reviews = browser.find_elements_by_css_selector(
                    "[class='shopee-product-rating']")
                # Get product review
                for product in product_reviews:
                    list_per_comment = []
                    # review = product.find_element_by_css_selector("[class='shopee-product-rating__content']").text
                    review = product.find_element_by_css_selector(
                        "[class='_3NrdYc']").text
                    day = product.find_element_by_css_selector(
                        "[class='shopee-product-rating__time']").text
                    day = day.split()
                    day = day[0]
                    if (review != "" or review.strip()):
                        print(review, "/n")
                        # list_review.append(review)
                        # list_time.append(day)
                        list_per_comment.append(day)
                        list_per_comment.append(review)
                        list_per_comment.append('shopee')
                        list_sum.append(list_per_comment)
                # Check for button next-pagination-item have disable attribute then jump from loop else click on the next button

                if len(browser.find_elements_by_css_selector(
                        "button.shopee-icon-button.shopee-icon-button--right[disabled]")) > 0:
                    break
                else:
                    button_next = WebDriverWait(browser, 5).until(EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "button.shopee-icon-button.shopee-icon-button--right")))
                    # driver.execute_script("arguments[0].click();", button_next)
                    button_next.click()
                    print("next page")
                    time.sleep(2)
                    x += 1

        except NoSuchElementException:
            browser.close()

        # list_sum=list(zip(list_time,list_review))
        # list_sum.append(list_per_comment)
        return list_sum

    data_shopee_top30 = []  # Lấy cmt top 30 sản phẩm bán nhiều nhất
    # temp=[]
    for i in range(30):
        data_shopee_top30.append(load_url_selenium_shopee(url=list_link[i]))
    # data_shopee.append(temp)

    list_shopee = []
    for i in range(len(data_shopee_top30)):
        df = pd.DataFrame(data_shopee_top30[i], columns=[
                          'time', 'comment', 'Source'])
        list_shopee.append(df)
    # df_shopee.head()
    df_shopee = pd.concat(list_shopee, axis=0, ignore_index=True)

    def time_convert(data):
        for index, i in enumerate(data.time.astype(str)):
            date = datetime.strptime(i.strip(), '%Y-%m-%d')
            data.time[index] = date

    time_convert(df_shopee)
    return df_shopee


data = crawling_data_voz('công nghệ')
print(data)
