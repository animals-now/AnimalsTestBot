from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import gspread


from datetime import datetime
import random
from random import randint
import string
from time import sleep

import sys
sys.path.append('/home/maor_animals_now_org/pytest')
from pytest import auth

def random_char(y):  # create random characters
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


def opendriver(site):  # open site in firefox and retuen driver value
    CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
    chrome_options = Options()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,chrome_options=chrome_options)
    driver.get(site)
    return driver


def insertinfo():  # insert info and click on the confrim check box
    placeholder = ["שם פרטי", "שם משפחה", "אימייל", "טלפון"]
    info = [fname, lname, email, phone]
    info_index = 0
    for i in placeholder:
        box = driver.find_element_by_xpath('//input[@placeholder="{}"]'.format(i))
        box.send_keys(info[info_index])
        info_index += 1
    confrim_checkbox = driver.find_element_by_xpath('//label[@id="tfa_168-L"][@class="label postField"]')
    confrim_checkbox.click()


def send():  # press on continue
    send_button = driver.find_element_by_id('tfa_148')
    send_button.click()


site = "https://etgar22.co.il/?utm_source=test&utm_medium=test&utm_campaign=test"
fname = "test+bot"
lname = random_char(3) + str(randint(1, 999))
email = fname + lname + "@animals-now.org"
phone = "050" + str(randint(1000000, 9999999))

# sign up for adult's etgar
driver = opendriver(site)
insertinfo()
sleep(1)
send()
driver.quit()
sleep(30)

# sign up for teen's etgar
driver = opendriver(site)
insertinfo()
teen_checkbox = driver.find_element_by_xpath('//label[@id="tfa_90-L"][@class="label postField"]')
teen_checkbox.click()
sleep(1)
send()
age_box = driver.find_element_by_xpath('//input[@placeholder="מה הגיל שלך?"]')
age_box.send_keys(str(randint(14, 17)))
send()
parent_box = driver.find_element_by_xpath('//input[@placeholder="מספר הטלפון של אחד ההורים"]')
parent_box.send_keys("050" + str(randint(1000000, 9999999)))
send()
driver.quit()


sleep(360)  # wait for the sign ups to insert in the sign ups form
client = auth.get_service_sheet()  # open google sheet API client

report_sheet = client.open("Report").sheet1  # open report sheet, will insert success or failure
sheet_list = ["אתגר 22 מבוגרים - 2019 (Responses)", "אתגר 22 נוער - 2019 (Responses)"]
for sheet in sheet_list:
    sign_up_sheet = client.open(sheet).sheet1  # open sign up form sheet
    time_now = str(datetime.today())[0:16]
    row_failed = [time_now, sheet, email, "Sign up failed: not found in the sheet"]
    row_succeed = [time_now, sheet, email, "Sign up succeed"]

    try:
        cell = sign_up_sheet.find(email)  # search if the test email found in sign up form sheet
        report_sheet.insert_row(row_succeed, 2)  # if found insert: time, form name, succeed
    except gspread.CellNotFound:
        report_sheet.insert_row(row_failed, 2)  # if found insert: time, form name, failed
