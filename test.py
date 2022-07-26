import telegram
import datetime as dt
import schedule
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os
import time


def sendMessage():
    options = webdriver.ChromeOptions()

    # 옵션 설정
    options.add_argument("headless")
    options.add_argument("no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("disable-gpu")  # 가속 사용 x
    options.add_argument("lang=ko_KR")  # 가짜 플러그인 탑재
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    )  # user-agent 이름 설정
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # 드라이버 위치 경로 입력
    driver = webdriver.Chrome(
        executable_path=ChromeDriverManager().install(), chrome_options=options
    )

    nowtime = (dt.datetime.now() - dt.timedelta(minutes=20)).strftime("%H:%M")
    print(nowtime)

    driver.get("https://quasarzone.com/bbs/qb_saleinfo")
    driver.implicitly_wait(3)

    board = driver.find_element_by_xpath(
        '//*[@id="frmSearch"]/div/div[3]/div[4]/table/tbody'
    )

    for_name = board.find_elements_by_css_selector(
        "tr > td > div > div.market-info-list-cont > p > a"
    )

    names = []
    links = []
    prices = []
    times = []

    for i in for_name:
        if i.text[-1].isdigit():
            text_arr = i.text.split(" ")[:-1]
            text = ""
            for j in text_arr:
                text += j + " "
            text = text[:-1]
            names.append(text)
        else:
            names.append(i.text)
        links.append(i.get_attribute("href"))

    for_price = board.find_elements_by_css_selector("span[class='text-orange']")

    for i in for_price:
        text_arr = i.text.split(" ")[1:-1]
        text = ""
        for j in text_arr:
            text += j + " "
        prices.append(text)

    for_time = board.find_elements_by_css_selector("span[class='date']")

    for i in for_time:
        times.append(i.text.strip())

    driver.get("https://quasarzone.com/bbs/qb_tsy")
    driver.implicitly_wait(3)

    board = driver.find_element_by_xpath(
        '//*[@id="frmSearch"]/div/div[2]/div[3]/table/tbody'
    )

    for_name = board.find_elements_by_css_selector(
        "tr > td > div > div.market-info-list-cont > p > a"
    )

    for i in for_name:
        if i.text[-1].isdigit():
            text_arr = i.text.split(" ")[:-1]
            text = ""
            for j in text_arr:
                text += j + " "
            text = text[:-1]
            names.append(text)
        else:
            names.append(i.text)
        links.append(i.get_attribute("href"))

    for_price = board.find_elements_by_css_selector("span[class='text-orange']")

    for i in for_price:
        text_arr = i.text.split(" ")[1:-1]
        text = ""
        for j in text_arr:
            text += j + " "
        prices.append(text)

    for_time = board.find_elements_by_css_selector("span[class='date']")

    for i in for_time:
        times.append(i.text.strip())

    driver.close()

    index = 0

    for i in range(len(times)):
        if times[i] < nowtime:
            index = i
            break

    names = names[:index]
    links = links[:index]
    prices = prices[:index]
    times = times[:index]

    result = ""

    for i in range(len(names)):
        result += names[i] + "\n" + links[i] + "\n" + prices[i] + "\n" + times[i]
        if i != len(names):
            result += "\n"

    if result == "":
        result = "20분 이내 새로 업데이트 된 항목이 없습니다."

    bot = telegram.Bot(token="{TOKEN}")
    chat_id = {CHAT_ID}

    bot.sendMessage(chat_id=chat_id, text=result)


schedule.every(20).minutes.do(sendMessage)

while True:
    schedule.run_pending()
    time.sleep(1)
