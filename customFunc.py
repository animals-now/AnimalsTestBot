from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import gspread

from datetime import datetime
import random
from random import randint
import string
from time import sleep

import emailfunc
import sys
sys.path.append('/home/maor_animals_now_org/pytest')
import auth

class webFunc:

    def __init__(self, site):
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
        self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,chrome_options=chrome_options)
        self.site = site

    def url(self):
        self.driver.execute_script("window.location = '{}'".format(self.site))

    @staticmethod
    def random_char(y):  # create random characters
        return ''.join(random.choice(string.ascii_letters) for x in range(y))

    def insertinfo(self):  # insert info and click on the confrim check box
        etgar = "https://etgar22.co.il/?utm_source=test&utm_medium=test&utm_campaign=test"
        ch = "https://challenge22.com/?utm_source=test&utm_medium=test&utm_campaign=test"
        ch_es = "https://challenge22.com/es/?utm_source=test&utm_medium=test&utm_campaign=test"
        fname = "test+bot"
        lname = webFunc.random_char(3) + str(randint(1, 999))
        email = fname + lname + "@animals-now.org"
        phone = "050" + str(randint(1000000, 9999999))
        self.info = [fname, lname, email, phone]
        info_index = 0
        if self.site == etgar:
            placeholder = ["שם פרטי", "שם משפחה", "אימייל", "טלפון"]
        elif self.site == ch:
            placeholder = ["First Name", "Last Name", "Email", " Phone (optional)"]
        elif self.site == ch_es:
            placeholder = ["Nombre", "Apellido", "Email", "Teléfono (opcional)"]
        else:  # for petitions
            placeholder = ["שם פרטי", "שם משפחה", "אימייל", "מספר טלפון"]

        for i in placeholder:
            box = self.driver.find_element_by_xpath('//input[@placeholder="{}"]'.format(i))
            box.send_keys(self.info[info_index])
            info_index += 1


    def collectinfo(self):
        return self.info

    def send(self):  # press on continue
        send_button = self.driver.find_element_by_id('tfa_148')
        send_button.click()

    def etgarconfirm(self):
        confrim_checkbox = self.driver.find_element_by_xpath('//label[@id="tfa_168-L"]')
        confrim_checkbox.click()

    def ch_confirm_sixteen(self):
        sixteen_checkbox = self.driver.find_element_by_xpath('//label[@id="tfa_93-L"]')
        sixteen_checkbox.click()

    def teen(self):
        teen_checkbox = self.driver.find_element_by_xpath('//label[@id="tfa_90-L"]')
        teen_checkbox.click()
        sleep(1)
        self.send()
        age_box = self.driver.find_element_by_xpath('//input[@placeholder="מה הגיל שלך?"]')
        age_box.send_keys(str(randint(14, 17)))
        self.send()
        parent_box = self.driver.find_element_by_xpath('//input[@placeholder="מספר הטלפון של אחד ההורים"]')
        parent_box.send_keys("050" + str(randint(1000000, 9999999)))


    def healthissue(self):
        etgar = "https://etgar22.co.il/?utm_source=test&utm_medium=test&utm_campaign=test"
        ch = "https://challenge22.com/?utm_source=test&utm_medium=test&utm_campaign=test"
        ch_es = "https://challenge22.com/es/?utm_source=test&utm_medium=test&utm_campaign=test"
        if self.site == etgar:
            general_issues_checkbox = self.driver.find_element_by_xpath('//label[@id="tfa_164-L"]')
            general_issues_checkbox.click()
            facebook_placeholder = "שם מלא ושם בפייסבוק"
        elif self.site == ch:
            general_issues_checkbox = self.driver.find_element_by_xpath('//label[@id="tfa_91-L"]')
            general_issues_checkbox.click()
            facebook_placeholder = "Full Name & Facebook Name"
        elif self.site == ch_es:
            general_issues_checkbox = self.driver.find_element_by_xpath('//label[@id="tfa_91-L"]')
            general_issues_checkbox.click()
            facebook_placeholder = "Nombre completo y nombre en Facebook"

        self.send()
        health_issues_id = ["tfa_96-L", "tfa_97-L", "tfa_98-L", "tfa_101-L", "tfa_102-L"]
        random_issue = random.choice(health_issues_id)
        specific_issues_checkbox = self.driver.find_element_by_xpath(
            '//label[@class="label postField"][@id="{}"]'.format(random_issue))
        specific_issues_checkbox.click()
        sleep(1)

        if random_issue == "tfa_97-L":  # "עברת ניתוח בריאטרי"
            time_pass_id = ["tfa_114-L", "tfa_113-L", "tfa_114-L"]
            random_time_pass = random.choice(time_pass_id)
            time_pass_checkbox = self.driver.find_element_by_xpath(
                '//label[@id="{}"]'.format(random_time_pass))
            time_pass_checkbox.click()
            if random_time_pass == "tfa_113-L":  # "מעל שנה (ללא סיבוכים מיוחדים)"
                pass
            else:  # "עד שנה, מעל שנה (עם סיבוכים מיוחדים)"
                facebook_name_box = self.driver.find_elements_by_xpath(
                    '//input[@placeholder = "{}"]'.format(facebook_placeholder))
                for box in facebook_name_box:
                    try:
                        box.send_keys("test+bot" + "bodek")
                    except:
                        pass
        else:  # "כל שאר המחלות"
            try:
                facebook_name_box = self.driver.find_elements_by_xpath(
                    '//input[@placeholder = "{}"]'.format(facebook_placeholder))
                for box in facebook_name_box:
                    try:
                        box.send_keys("test+bot" + "bodek")
                    except:
                        pass
            except:
                pass
                
    def check_in_sheets(self, sheet):
        client = auth.get_service_sheet()  # open google sheet API client
        service = auth.get_service_gmail() # open gmail Api
        report_sheet = client.open("Report").sheet1  # open report sheet, will insert success or failure
        self.sheet = sheet

        sign_up_sheet = client.open(self.sheet).sheet1  # open sign up form sheet
        time_now = str(datetime.today())[0:16]
        row_failed = [time_now, self.sheet, self.info[2], "Sign up failed: not found in the sheet"]
        row_succeed_all = [time_now, self.sheet, self.info[2], "Sign up succeed and removed from google sheet"]
        row_remove_more = [time_now, self.sheet, self.info[2], "Sign up succeed but remove more that one row"]
        row_not_remove = [time_now, self.sheet, self.info[2], "Sign up succeed but found test email"]
        try:
            sign_up_sheet.find(self.info[2])  # search if the test email found in sign up form sheet
            rows_before_delete = len(sign_up_sheet.col_values(1))
            sign_up_sheet.delete_row(sign_up_sheet.find(self.info[2]).row)
            rows_after_delete = len(sign_up_sheet.col_values(1))
            gap = str(rows_before_delete - rows_after_delete)
            row_failed.append(gap)  # adding the number of rows that remove
            row_succeed_all.append(gap)
            row_remove_more.append(gap)
            row_not_remove.append(gap)
            try:
                sign_up_sheet.find(self.info[2])  # try to find the test email again
                if rows_before_delete - rows_after_delete > 1:  # check if more then one row was delete
                    report_sheet.insert_row(row_remove_more, 2)  # report that more then one row was delete
                    report_sheet.insert_row(row_not_remove, 2)  # tell us the test email found after deleting
                    emailfunc.send_emails(service, row_remove_more)  # send email, open the func in order to see to who
                    emailfunc.send_emails(service, row_not_remove)
                else:
                    report_sheet.insert_row(row_not_remove, 2)  # tell us the test email found after deleting
                    emailfunc.send_emails(service, row_not_remove)
            except gspread.CellNotFound:
                if rows_before_delete - rows_after_delete > 1:  # check if more then one row was delete
                    report_sheet.insert_row(row_remove_more, 2)  # report that more then one row was delete
                    emailfunc.send_emails(service, row_remove_more)
                else:
                    report_sheet.insert_row(row_succeed_all, 2)  # tell us that everything work right
        except gspread.CellNotFound:
            report_sheet.insert_row(row_failed, 2)  # tell us that test email didn't found in the sheet
            emailfunc.send_emails(service, row_failed)            


    def petitions_age(self):
        age_box = self.driver.find_element_by_xpath('//select[@placeholder="שנת לידה"]')
        age_box.click()
        select_age = self.driver.find_element_by_xpath('//option[@value="{}"]'.format(randint(1930, 2004)))
        select_age.click()

    def petitions_send(self):  # press on continue
        send_button = self.driver.find_element_by_xpath('//button[@type="submit"]')
        send_button.click()

    def check_in_gmail(self, email_list, petitions_list):  # check for if user got thank you email and if we got email
        # from salesforce
        service = auth.get_service_gmail()  # open gmail API client
        client = auth.get_service_sheet()  # open google sheet API client
        report_sheet = client.open("Report").sheet1  # open report sheet, will insert success or failure

        petitions_index = 0
        for email_address in email_list:
            status = emailfunc.two_emails(service, 'me', email_address)
            row_status = [str(datetime.today())[0:16], petitions_list[petitions_index], email_address, status]
            report_sheet.insert_row(row_status, 2)
            petitions_index += 1
            if status != "Succeed! Thanks email and Salesforce email received":
                emailfunc.send_emails(service, row_status)

