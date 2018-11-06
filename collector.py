from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta

import time

TIME_A_DAY_BEFORE = timedelta(days=1)
TIME_TODAY = datetime.today()
INITIAL_URL = 'https://entertain.naver.com/ranking#type=hit_total&date='


def main():
    print_initial_comment()

    chrome_driver = load_driver('./Chrome_driver/win32/chromedriver.exe', 'chrome')

    for ii in range(0, 31):
        for list_num in range(1, 31):

            print("COLLECT %s's RANK-%s COMMENTS" % (
                (TIME_TODAY - ii * TIME_A_DAY_BEFORE).strftime('%Y-%m-%d'), list_num))

            get_url_page = chrome_driver.get(INITIAL_URL + (TIME_TODAY - ii * TIME_A_DAY_BEFORE).strftime('%Y-%m-%d'))
            time.sleep(0.5)
            click_ranking_news = chrome_driver.find_element_by_css_selector(
                '#ranking_list > li:nth-child(%s) > div.tit_area > a' % list_num)
            click_ranking_news.click()
            time.sleep(0.5)
            chrome_driver.implicitly_wait(0.5)

            try:
                click_show_comment_btn = chrome_driver.find_element_by_xpath(
                    '//*[@id="cbox_module"]/div[2]/div[9]/a/span[1]')
                click_show_comment_btn.click()
            except:
                click_show_comment_btn = chrome_driver.find_element_by_xpath('//*[@id="cbox_module"]/div/div/a[1]')
                click_show_comment_btn.click()
            time.sleep(0.5)

            more_comment = chrome_driver.find_element_by_xpath('//*[@id="cbox_module"]/div/div[8]/a')

            while True:
                try:
                    for ii in range(0,9):
                        more_comment.click()
                    break
                except:
                    break

            comments_list, title = collect_all_comments_and_title(chrome_driver)
            save_comment_and_title_to_file(comments_list, title)

    chrome_driver.close()


def save_comment_and_title_to_file(comments_list, title):
    TIME_NOW = int(time.time())
    fp = open('./collected/' + str(TIME_NOW) + '.txt', 'w', encoding='utf-8')
    fp.writelines('#' * 6 + 'TITLE : ' + title + 'NUM : ' + str(len(comments_list)) + '#' * 6 + '\r\n')
    for comment in comments_list:
        fp.writelines(comment.text + '\r\n')

    fp.close()


def collect_all_comments_and_title(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')
    title = soup.find('p', {'class': 'end_tit'}).text
    print(title)
    comments = soup.find_all("span", {"class": "u_cbox_contents"})
    print(len(comments))

    return (comments, title)


def print_initial_comment():
    print('#' * 40 + TIME_TODAY.strftime('%y-%m-%d') + '#' * 41)
    print('*' * 30 + 'NAVER COMMENTS COLLECTOR' + '*' * 30 + '\n' + '::initial_url : ' + INITIAL_URL)
    print('#' * 90)


def load_driver(driver_path, driver_type):
    if (driver_type == 'chrome'):
        driver = webdriver.Chrome(driver_path)
    elif (driver_type == 'phantomjs'):
        driver = webdriver.PhantomJS(driver_path)
    else:
        print('not supported driver')
        exit()
    return driver


if __name__ == '__main__':
    main()
