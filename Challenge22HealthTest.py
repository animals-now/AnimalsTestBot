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



site = "https://challenge22.com/?utm_source=test&utm_medium=test&utm_campaign=test"
fname = "test+bot"
lname = random_char(3) + str(randint(1, 999))
email = fname + lname + "@animals-now.org"
phone = "050" + str(randint(1000000, 9999999))

random_time_pass = None
driver = opendriver(site)
insertinfo()
general_issues_checkbox = driver.find_element_by_xpath('//label[@id="tfa_91-L"]')
general_issues_checkbox.click()
send()
health_issues_id = ["tfa_96-L", "tfa_97-L", "tfa_98-L", "tfa_101-L", "tfa_102-L", ]
random_issue = random.choice(health_issues_id)
specific_issues_checkbox = driver.find_element_by_xpath('//label[@class="label postField"][@id="{}"]'.format(random_issue))
specific_issues_checkbox.click()
sleep(1)

try:
    time_pass_id = ["tfa_112-L", "tfa_113-L", "tfa_114-L"]
    random_time_pass = random.choice(time_pass_id)
    time_pass_checkbox = driver.find_element_by_xpath(
        '//label[@class="label postField"][@id="{}"]'.format(random_time_pass))
    time_pass_checkbox.click()
    try:
        sleep(1)
        facebook_name_box = driver.find_elements_by_xpath('//input[@placeholder="Full Name & Facebook Name"]')
        for box in facebook_name_box:
            try:
                box.send_keys(fname + lname)
            except:
                pass
        send()
    except:
        sleep(1)
        send()
except:
    try:
        sleep(1)
        facebook_name_box = driver.find_elements_by_xpath('//input[@placeholder="Full Name & Facebook Name"]')
        for box in facebook_name_box:
            try:
                box.send_keys(fname + lname)
            except:
                pass
        send()
    except:
        try:
            sleep(1)
            send()
        except:
            if random_time_pass == None:
                reason_to_failure = ["Could not complete sign up Etgar health issues:", "Selected issue", str(random_issue)]
            else:
                reason_to_failure = ["Could not complete sign up Etgar health issues:", "Selected issue:", str(random_issue),
                                     str(random_time_pass)]
            client = auth.get_service_sheet()  # open google sheet API client
            report_sheet = client.open("Report").sheet1  # open report sheet, will insert success or failure
            report_sheet.insert_row(reason_to_failure, 2)
sleep(3)
driver.quit()

sleep(400)  # wait for the sign ups to insert in the sign ups form
client = auth.get_service_sheet()  # open google sheet API client

report_sheet = client.open("Report").sheet1  # open report sheet, will insert success or failure

sheet = " הרשמה לאתגר 22 - ENGLISH HEALTH"
sign_up_sheet = client.open(sheet).sheet1  # open sign up form sheet
time_now = str(datetime.today())[0:16]
row_failed = [time_now, sheet, email, "Sign up failed: not found in the sheet", random_issue, random_time_pass]
row_succeed = [time_now, sheet, email, "Sign up succeed", random_issue, random_time_pass]

try:
    cell = sign_up_sheet.find(email)  # search if the test email found in sign up form sheet
    report_sheet.insert_row(row_succeed, 2)  # if found insert: time, form name, succeed
except gspread.CellNotFound:
    report_sheet.insert_row(row_failed, 2)  # if found insert: time, form name, failed