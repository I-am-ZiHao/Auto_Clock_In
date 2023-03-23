from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json
from bs4 import BeautifulSoup
import urllib.request
import time
from openpyxl import load_workbook
from openpyxl import Workbook
from datetime import date, datetime
import random
from apscheduler.schedulers.blocking import BlockingScheduler

def work():

    current_date_and_time = datetime.now()
    current_hour = current_date_and_time.hour

    if current_hour >= 17:  # 下班
        min_to_start = random.randint(11, 20)
    else:  # 上班
        min_to_start = random.randint(1, 10)
    time.sleep(min_to_start * 60)
    
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')

    singin_url = "https://my.ntu.edu.tw/attend/ssi.aspx?from=signNote"
    driver = webdriver.Chrome(chrome_options=chrome_options)  #webdriver.Chrome()
    web = driver.get(singin_url)

    try:
        login_button = driver.find_element_by_id("divLogin")
        login_button.click()

        name = driver.find_element_by_name("user")
        name.send_keys("account")

        password = driver.find_element_by_name("pass")
        password.send_keys("password")

        login_button = driver.find_element_by_name("Submit")
        login_button.click()
    except:
        with open('record.txt','a') as f:
            f.write('no need to login again. ')
            f.close()

    try:
        if current_hour >= 17:  # 下班
            login_button = driver.find_element_by_id("btSign2")
            login_button.click()
        else:  # 上班
            login_button = driver.find_element_by_id("btSign")
            login_button.click()
    except:
        with open('record.txt','a') as f:
            f.write('failed at ')
            f.close()

    with open('record.txt','a') as f:
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
        f.close()

    driver.close()

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(work, 'cron', minute="00",hour="8,17",day_of_week="mon-fri")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
