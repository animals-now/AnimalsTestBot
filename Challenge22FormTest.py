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
import auth


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

def insertinfo(): # insert info and click on the confrim check box
    box_id_list = ["tfa_1_0", "tfa_2_0", "tfa_3_0", "tfa_4_0"]
    info = [fname, lname, email, phone]
    info_index = 0
    for i in box_id_list:
        box = driver.find_element_by_xpath('//input[@id="{}"]'.format(i))
        box.send_keys(info[info_index])
        info_index += 1
    sixteen_checkbox = driver.find_element_by_xpath('//label[@id="tfa_93-L"][@class="label postField"]')
    sixteen_checkbox.click()
def send(): #press on continue
    send_button = driver.find_element_by_id('tfa_148')
    send_button.click()

ch = "https://challenge22.com/?utm_source=test&utm_medium=test&utm_campaign=test"
ch_es = "https://challenge22.com/es/?utm_source=test&utm_medium=test&utm_campaign=test"
site_list = [ch, ch_es]
fname = "test+bot"
lname = random_char(3) + str(randint(1, 999))
email = fname + lname + "@animals-now.org"
phone = "050" + str(randint(1000000, 9999999))

for site in site_list:
    driver = opendriver(site)
    insertinfo()
    sleep(1)
    send()
    driver.quit()
    sleep(30)


sleep(280)
client = auth.get_service_sheet()

report_sheet = client.open("Report").sheet1
sheet_list = ["הרשמה לאתגר 22 -  ENGLISH NEW ", "הרשמה לאתגר 22 - SPANISH"]
for sheet in sheet_list: # Insert if the test failed or succeed for each form
    sign_up_sheet = client.open(sheet).sheet1
    time_now = str(datetime.today())[0:16]
    row_failed = [time_now, sheet, email, "Sign up failed: not found in the sheet"]
    row_succeed = [time_now, sheet, email, "Sign up succeed"]

    try:
        cell = sign_up_sheet.find(email)
        report_sheet.insert_row(row_succeed, 2)
    except gspread.CellNotFound:
        report_sheet.insert_row(row_failed, 2)