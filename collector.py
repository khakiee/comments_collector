import datetime
import time
from datetime import timedelta

from bs4 import BeautifulSoup
from selenium import webdriver

import values as val

TIME_A_DAY = timedelta(days=1)

URL_LIST = [val.ENT_URL, val.POL_URL, val.ECO_URL, val.SOC_URL]
CATEGORY_LIST = ['Entertain', 'Politics', 'Economic', 'Social']

MAX_RANK = 30
MAX_LOOP_SHOW_MORE_BTN = 10


def main():
    print_initial_comment()
    check_values_isvalid()

    category = init_menu_and_select_category()
    start_date, end_date = create_date_data(category)

    chrome_driver = load_driver('./chromedriver', 'chrome')

    while True:

        if start_date > end_date:
            break
        start_date_str = create_strf_date(start_date, category)

        for list_num in range(1, MAX_RANK + 1):
            chrome_driver.get(URL_LIST[category] + start_date_str)
            time.sleep(0.5)

            click_ranking_news(chrome_driver, category, list_num)
            time.sleep(0.5)

            click_show_comments(chrome_driver, category)
            time.sleep(0.5)

            click_more_comment(chrome_driver, category, MAX_LOOP_SHOW_MORE_BTN)
            time.sleep(0.5)

            comments_list, title = collect_all_comments_and_title(chrome_driver, category)
            save_comment_and_title_to_file(comments_list, title, category)

        start_date += TIME_A_DAY

    chrome_driver.close()
    print('#' * 10 + 'ALL DONE' + '#' * 10)


def save_comment_and_title_to_file(comments_list, title, category):
    TIME_NOW = int(time.time())

    fp = open('./collected/' + CATEGORY_LIST[category] + '_' + str(TIME_NOW) + '.txt', 'w', encoding='utf-8')
    fp.writelines('#' * 6 + 'TITLE : ' + title + 'NUM : ' + str(len(comments_list)) + '#' * 6 + '\r\n')

    for comment in comments_list:
        fp.writelines(comment.text + '\r\n')

    fp.close()


def collect_all_comments_and_title(driver, category):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')

    if category > 0:
        title = soup.find('h3', {'id': 'articleTitle'}).text
    elif category == 0:
        title = soup.find('p', {'class': 'end_tit'}).text

    print(title)
    comments = soup.find_all("span", {"class": "u_cbox_contents"})
    print(len(comments))

    return (comments, title)


def print_initial_comment():
    print('#' * 40 + '' + '#' * 41)
    print('*' * 30 + 'NAVER COMMENTS COLLECTOR' + '*' * 30)
    print('0.1.2')
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


def init_menu_and_select_category():
    print("(ent, pol, eco, soc) category : ")
    category_dict = {"ent": 0, "pol": 1, "eco": 2, "soc": 3}
    try:
        category = category_dict[input()]
    except:
        print("wrong category")
        exit()

    return category


def create_date_data(category):
    print("choose period (ex. 2018-11-06 2018-11-08) : ")

    collect_period = input()
    start_date, end_date = collect_period.split(' ')

    start_date = start_date.split('-')
    start_date = datetime.date(int(start_date[0]), int(start_date[1]), int(start_date[2]))

    end_date = end_date.split('-')
    end_date = datetime.date(int(end_date[0]), int(end_date[1]), int(end_date[2]))

    print("Start collecting -- %s | %s ~ %s" % (CATEGORY_LIST[category], start_date, end_date))

    return (start_date, end_date)


def create_strf_date(start_date, category):
    # 연예 뉴스와 그 외 뉴스 페이지의 url date format이 다르기 때문에 구분
    if category > 0:
        start_date_str = start_date.strftime('%Y%m%d')
    elif category == 0:
        start_date_str = start_date.strftime('%Y-%m-%d')

    return start_date_str


def click_ranking_news(driver, category, list_num):
    # 연예 뉴스와 그 외 뉴스 페이지의 ranking list의 css selecor 값이 다름
    # TODO : xpath로 변경
    if category > 0:
        click_ranking_news = driver.find_element_by_css_selector(
            '#wrap > table > tbody > tr > td.content > div > div.ranking > '
            'ol > li.ranking_item.is_num%s > div.ranking_text '
            '> div.ranking_headline > a' % str(list_num))
        click_ranking_news.click()

    elif category == 0:
        click_ranking_news = driver.find_element_by_css_selector(
            '#ranking_list > li:nth-child(%s) > div.tit_area > a' % list_num)
        click_ranking_news.click()


def click_show_comments(driver, category):
    # 연예 뉴스와 그 외 뉴스의 '댓글 더보기' 버튼의 xpath 값이 다르기 때문에 구분
    if category > 0:
        # 정치, 경제, 사회 뉴스에서 외부 뉴스와 네이버 뉴스의 '댓글 더보기 버튼이 다르기 때문에 구분
        try:
            click_show_comments = driver.find_element_by_xpath('//*[@id="cbox_module"]/div[2]/div[9]/a')
            click_show_comments.click()
        except:
            click_show_comments = driver.find_element_by_xpath(
                '//*[@id="cbox_module"]/div/div/a[1]')
            click_show_comments.click()
    elif category == 0:
        # 연예 뉴스에서 외부 뉴스와 네이버 뉴스의 '댓글 더보기' 버튼이 다르기 때문에 구분
        try:
            click_show_comments = driver.find_element_by_xpath(
                '//*[@id="cbox_module"]/div[2]/div[9]/a/span[1]')
            click_show_comments.click()
        except:
            click_show_comments = driver.find_element_by_xpath('//*[@id="cbox_module"]/div/div/a[1]')
            click_show_comments.click()


def click_more_comment(driver, category, loop_num):
    # 연예 뉴스와 그 외 뉴스의 '더보기' 버튼의 xpath 가 다르기 때문에 구분
    if category > 0:
        # 정치, 경제, 사회 에서 네이버 뉴스와 외부 뉴스의 '더보기' 버튼의 xpath가 다르기 때문에 구분
        try:
            more_comment = driver.find_element_by_xpath('//*[@id="cbox_module"]/div[2]/div[9]/a')
        except:
            more_comment = driver.find_element_by_xpath('//*[@id="cbox_module"]/div/div[9]/a')
    elif category == 0:
        more_comment = driver.find_element_by_xpath('//*[@id="cbox_module"]/div/div[8]/a')

    while True:
        try:
            for ii in range(0, loop_num):
                more_comment.click()
            break
        except:
            # '더보기' 버튼 클릭 불가 시 (더 볼 댓글이 없는 상태) 강제 break
            break


def check_values_isvalid():
    if MAX_RANK > 30 or MAX_RANK < 1:
        print('MAXRANK is not valid value (integer 1~30)')

    if URL_LIST == None:
        print('URL_LIST is empty')


if __name__ == '__main__':
    main()
