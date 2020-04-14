from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import auth
import emailfunc

from datetime import datetime
import random
from random import randint
import string
from time import sleep


def random_char(y): # create random character
    return ''.join(random.choice(string.ascii_letters) for x in range(y))

def opendriver(site): # open site in firefox and retuen driver value
    driver = webdriver.Firefox(executable_path="C:\webdrivers\geckodriver.exe")
    driver.get(site)
    return driver

def insertinfo(): # insert info and click on the confrim check box
    box_id_list = ["tfa_1_0", "tfa_2_0", "tfa_3_0", "tfa_4_0"]
    info = [fname, lname, email, phone]
    info_index = 0
    for i in box_id_list:
        box = driver.find_element_by_xpath('//input[@id="{}"]'.format(i))
        box.send_keys(info[info_index])
        info_index +=1
    sixteen_checkbox = driver.find_element_by_xpath('//label[@id="tfa_93-L"][@class="label postField"]')
    sixteen_checkbox.click()
def send(): #press on continue
    send_button = driver.find_element_by_id('tfa_148')
    send_button.click()

ch = "https://challenge22.com/?utm_source=test&utm_medium=test&utm_campaign=test"
ch_es = "https://challenge22.com/es/?utm_source=test&utm_medium=test&utm_campaign=test"
site_list = [ch, ch_es]
fname = "test"
lname = random_char(3)+str(randint(1,999))
email = fname + lname + "@email.com"
phone = "050" + str(randint(1000000, 9999999))

for site in site_list:
    driver = opendriver(site)
    insertinfo()
    send()
    driver.quit()


sleep(240)
client = auth.get_service_sheet()

report_sheet = client.open("Report").sheet1
sheet_list = ["CH22 SHEET", "CH22 ES SHEET"]
for sheet in sheet_list: # Insert if the test failed or succeed for each form
    sign_up_sheet = client.open(sheet).sheet1
    time_now = str(datetime.today())[0:16]
    row_failed = [time_now, sheet, email, "Sign up failed"]
    row_succeed = [time_now, sheet, email, "Sign up succeed"]

    try:
        cell = sign_up_sheet.find(email)
        report_sheet.insert_row(row_succeed, 2)
    except gspread.CellNotFound:
        report_sheet.insert_row(row_failed, 2)