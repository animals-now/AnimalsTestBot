from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import auth

from datetime import datetime
import random
from random import randint
import string
from time import sleep


def random_char(y): # create random characters
    return ''.join(random.choice(string.ascii_letters) for x in range(y))

def opendriver(site): # open site in firefox and retuen driver value
    driver = webdriver.Firefox(executable_path="C:\webdrivers\geckodriver.exe")
    driver.get(site)
    return driver

def insertinfo(): # insert info and click on the confrim check box
    placeholder = ["שם פרטי", "שם משפחה", "אימייל", "טלפון"]
    info = [fname, lname, email, phone]
    info_index = 0
    for i in placeholder:
        box = driver.find_element_by_xpath('//input[@placeholder="{}"]'.format(i))
        box.send_keys(info[info_index])
        info_index +=1
    confrim_checkbox = driver.find_element_by_xpath('//label[@id="tfa_168-L"][@class="label postField"]')
    confrim_checkbox.click()
def send():# press on continue
    send_button = driver.find_element_by_id('tfa_148')
    send_button.click()

site = "https://etgar22.co.il/?utm_source=test&utm_medium=test&utm_campaign=test"
fname = "test"
lname = random_char(3)+str(randint(1,999))
email = fname + lname + "@email.com"
phone = "050" + str(randint(1000000, 9999999))


# sign Up for adult etgar
driver = opendriver(site)
insertinfo()
send()
driver.quit()

# sign Up for teen challenge
driver = opendriver(site)
insertinfo()
teen_checkbox = driver.find_element_by_xpath('//label[@id="tfa_90-L"][@class="label postField"]')
teen_checkbox.click()
send()
age_box = driver.find_element_by_xpath('//input[@placeholder="מה הגיל שלך?"]')
age_box.send_keys(str(randint(14,17)))
send()
parent_box = driver.find_element_by_xpath('//input[@placeholder="מספר הטלפון של אחד ההורים"]')
parent_box.send_keys("050" + str(randint(1000000,9999999)))
send()
driver.quit()


sleep(240) # wait for the sign ups to insert in the sign ups form
client = auth.get_service_sheet() # open google sheet API client

report_sheet = client.open("Report").sheet1 # open report sheet, will insert success or failure
sheet_list = ["אתגר 22 מבוגרים - 2019 (Responses)", "אתגר 22 נוער - 2019 (Responses)"]
for sheet in sheet_list:
    sign_up_sheet = client.open(sheet).sheet1 # open sign up form sheet

    row_failed = [str(datetime.now()), sheet, email, "Sign up failed"]
    row_succeed = [str(datetime.now()), sheet, email, "Sign up succeed"]

    try:
        cell = sign_up_sheet.find(email) # search if the test email found in sign up form sheet
        report_sheet.insert_row(row_succeed, 2)# if found insert: time, form name, succeed
    except gspread.CellNotFound:
        report_sheet.insert_row(row_failed, 2)# if found insert: time, form name, failed