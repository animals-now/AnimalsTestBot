from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import gspread
import emailfunc

from datetime import datetime
from random import randint
from time import sleep

import sys
sys.path.append('/home/maor_animals_now_org/pytest')
import auth



def random_char(length):
    letters = "abcdefghijklmnopqrstuvwxyz"
    chars = ''
    for x in range(length):
        chars += chars.join(letters[randint(0, 25)])
    return chars

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
    placeholder = ["שם פרטי", "שם משפחה", "אימייל", "מספר טלפון"]
    info = [fname, lname, email, phone]
    info_index = 0
    for i in placeholder:
        box = driver.find_element_by_xpath('//input[@placeholder="{}"]'.format(i))
        box.send_keys(info[info_index])
        info_index += 1
    age_box = driver.find_element_by_xpath('//select[@placeholder="שנת לידה"]')
    age_box.click()
    select_age = driver.find_element_by_xpath('//option[@value="{}"]'.format(randint(1930, 2004)))
    select_age.click()


def send():  # press on continue
    send_button = driver.find_element_by_xpath('//button[@type="submit"]')
    send_button.click()


turkey = "https://animals-now.org/investigations/turkey/?utm_source=test&utm_medium=test&utm_campaign=test"
live_transports = "https://animals-now.org/issues/live-transports/?utm_source=test&utm_medium=test&utm_campaign=test"
cages = "https://animals-now.org/issues/cages/?utm_source=test&utm_medium=test&utm_campaign=test"
protection_act = "https://animals-now.org/issues/animal-protection-act/?utm_source=test&utm_medium=test&utm_campaign=test"
fish = "https://animals-now.org/investigations/fish/?utm_source=test&utm_medium=test&utm_campaign=test"
zoglobek = "https://animals-now.org/issues/zoglobek-lawsuit/?utm_source=test&utm_medium=test&utm_campaign=test"
fur = "https://animals-now.org/issues/fur/?utm_source=test&utm_medium=test&utm_campaign=test"

site_list = [turkey] # , live_transports, cages, protection_act, fish, zoglobek, fur]
fname = "test+bot"
email_list = []  # list with the email used to sign up
petitions_list = []  # list with link to petition that the bot signed up
for site in site_list:  # sign up to petitions in the site list, for each sign up generate new info
    lname = random_char(3) + str(randint(1, 999))
    email = fname + lname + "@animals-now.org"
    phone = "050" + str(randint(1000000, 9999999))
    driver = opendriver(site)
    insertinfo()
    sleep(1)
    send()
    driver.quit()
    email_list.append(email)
    petitions_list.append(site)
    sleep(30)

sleep(30)
service = auth.get_service_gmail()  # open gmail API client
client = auth.get_service_sheet()  # open google sheet API client
report_sheet = client.open("Report").sheet1  # open report sheet, will insert success or failure

petitions_index = 0
for email_address in email_list:
    status = emailfunc.two_emails(service, 'me', email_address)
    row_status = [str(datetime.today())[0:16], petitions_list[petitions_index], email_address, status]
    report_sheet.insert_row(row_status, 2)
    petitions_index += 1
