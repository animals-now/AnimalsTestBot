from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import gspread

from datetime import datetime
import random
from random import randint
from time import sleep

import emailfunc
import sys
sys.path.append('/home/maor_animals_now_org/pytest')
import auth


class webFunc:

    def __init__(self, site):
        self.site = site
        self.first_name = "test+bot"
        self.last_name = webFunc.random_char(5) + str(randint(1, 999))
        self.email = self.first_name + self.last_name + "@animals-now.org"
        self.phone = "052" + str(randint(1000000, 9999999))
        self.info = [self.first_name, self.last_name, self.email, self.phone]

    def start_driver(self):
        """
        Determine and start the selenium webdriver.
        """
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
        self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

    def url(self):
        """
        Navigate to the site address that accepted upon creating instance.
        """
        self.driver.execute_script("window.location = '{}'".format(self.site))

    @staticmethod
    def random_char(length):
        """
        Generate random alpha string, accept length of the string.
        """
        letters = "abcdefghijklmnopqrstuvwxyz"
        chars = ''
        for x in range(length):
            chars += chars.join(letters[randint(0, 25)])
        return chars

    def insert_info_to_field(self, field, keys):
        """
        The function find all element with <input> tag and search in each element for placeholder
        attribute. than check if any of placeholder_dict[field] is substring of placeholder value,
        if it does send keys to this element. If the function failed or succeed to send keys to this element,
        it will print massage to the console.
        accept:
        field - field to send keys
        keys - keys to send
        The function base on placeholder, if your form doesn't have placeholder,
        it won't work.
        """

        placeholder_dict = {'FirstName': ['פרטי', 'First', 'first', 'Nombre', 'nombre'],
                            'LastName': ['משפחה', 'Last', 'last', 'Apellido', 'apellido'],
                            'Email': ['אימייל', 'מייל', 'דוא"ל', 'דואר אלקטרוני', "דוא'ל", 'Email', 'email',
                                      'Correo electrónico', 'correo electrónico'],
                            'Phone': ['טלפון', 'נייד', 'Phone', 'phone', 'Mobile', 'mobile', 'Teléfono', 'teléfono',
                                      'Móvil', 'móvil'],
                            'Age': ['גיל', 'Age', 'age', 'Años', 'años'],
                            'Birthday': ['שנת לידה', 'Birthday', 'birthday', 'Cumpleaños', 'cumpleaños'],
                            'FullName': ['שם מלא', 'שם', 'Full name', 'full name', 'Name', 'name',
                                         'Nombre completo', 'nombre completo', 'Nombre', 'nombre'],
                            }

        # Find all elements with input tag (in the html <input>....</input>)
        input_elem_list = self.driver.find_elements_by_tag_name('input')
        for elem in input_elem_list:
            # Get the value of the placeholder inside input (<input>placeholder="some-value"</input>
            real_placeholder = elem.get_attribute('placeholder')
            # If any of the item inside placeholder_dict[field] are also inside the real_placeholder,
            # it will send keys to this element(field).
            if any([plc in real_placeholder for plc in placeholder_dict[field]]):
                try:
                    elem.send_keys(keys)
                    print('Succeed to send keys to: "{}" (field placeholder)'.format(real_placeholder))
                except:
                    print('Failed to send keys to: "{}" (field placeholder)'.format(real_placeholder))


    def send(self):
        """
        Click on "Submit/Continue" button in etgar22.co.il,in challenge22.com and in challenge22.com/es
        """
        send_button = self.driver.find_element_by_id('tfa_148')
        send_button.click()

    def etgarconfirm(self):
        """
        Click on "I accept the Term of use" check box in etgar22.co.il
        """
        confrim_checkbox = self.driver.find_element_by_xpath('//label[@id="tfa_168-L"]')
        confrim_checkbox.click()

    def ch_confirm_sixteen(self):
        """
        Click on "I am 16 or older and have read the Terms of Use" check box
        in challenge22.com and in challenge22.com/es
        """
        sixteen_checkbox = self.driver.find_element_by_xpath('//label[@id="tfa_93-L"]')
        sixteen_checkbox.click()


    def teen_check_box(self):
        """
        Click on "I am less that 18 year old" check box in etgar22.co.il
        """
        teen_checkbox = self.driver.find_element_by_xpath('//label[@id="tfa_90-L"]')
        teen_checkbox.click()


    def healthissue(self):
        """
        Sign ups to challenges's websites with random health.
        OLD FUNCTION CHECK IT BEFORE USING!!!
        """
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
        """
        Some of the signed ups transfer to google sheet, this function check if the registration arrived to
        the google sheet. If it does, the registration delete from the google sheet.
        If the registration doesn't arrive to the google sheet, failure email will be sent to dev.
        Also there is a method that check if there only one row deleted from the google sheet, in case more or
        less then one row deleted the test failed and email sent to dev.
        Also write registration detail in google sheet named 'Report'(test@animals-now.org is the owner of this sheet)
        """
        client = auth.get_service_sheet()  # open google sheet API client
        service = auth.get_service_gmail()  # open gmail Api
        report_sheet = client.open("Report").sheet1  # open report sheet, will insert success or failure
        self.sheet = sheet

        row_failed_msg = "Registration's email not found in google sheet!!!"
        row_success_all_msg = "Sign up succeed and removed from google sheet"
        row_remove_more_msg = "Sign up succeed but the bot removed more than one row in the google sheet!!!"
        row_not_remove_msg = "Sign up succeed but the bot failed to remove the test email from the google sheet"
        sign_up_sheet = client.open(self.sheet).sheet1  # open sign up form sheet
        time_now = str(datetime.today())[0:16]
        row_failed = [time_now, self.sheet, self.email, row_failed_msg]
        row_succeed_all = [time_now, self.sheet, self.email, row_success_all_msg]
        row_remove_more = [time_now, self.sheet, self.email, row_remove_more_msg]
        row_not_remove = [time_now, self.sheet, self.email, ]

        try:
            sign_up_sheet.find(self.email)  # search if the test email found in sign up form sheet
            rows_before_delete = len(sign_up_sheet.col_values(1))
            sign_up_sheet.delete_row(sign_up_sheet.find(self.email).row)
            rows_after_delete = len(sign_up_sheet.col_values(1))
            gap = str(rows_before_delete - rows_after_delete)
            row_failed.append(gap)  # adding the number of rows that remove
            row_succeed_all.append(gap)
            row_remove_more.append(gap)
            row_not_remove.append(gap)
            try:
                sign_up_sheet.find(self.email)  # try to find the test email again
                if rows_before_delete - rows_after_delete > 1:  # check if more then one row was delete
                    report_sheet.insert_row(row_remove_more, 2)  # report that more then one row was delete
                    report_sheet.insert_row(row_not_remove, 2)  # tell us the test email found after deleting
                    emailfunc.signup_failed_email(service,
                                                  row_remove_more)  # send email, open the func in order to see to who
                    emailfunc.signup_failed_email(service, row_not_remove)
                else:
                    report_sheet.insert_row(row_not_remove, 2)  # tell us the test email found after deleting
                    emailfunc.signup_failed_email(service, row_not_remove)
            except gspread.CellNotFound:
                if rows_before_delete - rows_after_delete > 1:  # check if more then one row was delete
                    report_sheet.insert_row(row_remove_more, 2)  # report that more then one row was delete
                    emailfunc.signup_failed_email(service, row_remove_more)
                else:
                    report_sheet.insert_row(row_succeed_all, 2)  # tell us that everything work right
        except gspread.CellNotFound:
            report_sheet.insert_row(row_failed, 2)  # tell us that test email didn't found in the sheet
            emailfunc.signup_failed_email(service, row_failed)


    def petitions_send(self):
        """
        Click on "Submit/Continue" button in animals-now.org's petitions
        """
        send_button = self.driver.find_element_by_css_selector('div #form_petition-form button.frm_button_submit')
        send_button.click()

    def check_in_gmail(self, email_list, petitions_list):
        """
        When petition registration success, the user's details transfer to salesforce. if salesforce receive
        email with this form: test+???@animals-now.org, salesforce will send the user details to
        test@animals-now.org.
        This function search in test@animals-now.org inbox for email from saleforce
        with the user's details, if the email not found the test failed and email about the failure will be send.
        Also write registration detail in google sheet named 'Report'(test@animals-now.org is the owner of this sheet)
        accept:
        email_list - list of email that the bot used to sign ups.
        petitions_list - list of petitions url the bot signed up.
        """
        service = auth.get_service_gmail()  # open gmail API client
        client = auth.get_service_sheet()  # open google sheet API client
        report_sheet = client.open("Report").sheet1  # open report sheet, will insert success or failure

        petitions_index = 0
        for email_address in email_list:
            num_emails_received = emailfunc.petition_emails(service, 'me', email_address)
            if num_emails_received == 1:
                status = "Succeed! Salesforce email received"
            else:
                status = "Failed - Found " + str(num_emails_received) + " emails instead of 1"
            row_status = [str(datetime.today())[0:16], petitions_list[petitions_index], email_address, status]
            report_sheet.insert_row(row_status, 2)
            if num_emails_received != 1:
                emailfunc.signup_failed_email(service, row_status)
            petitions_index += 1

    # def petitions_age(self):
    #     """
    #     Choose random birthday from the scroll in animals-now.org's petitions
    #     """
    #     age_box = self.driver.find_element_by_xpath('//select[@placeholder="שנת לידה"]')
    #     age_box.click()
    #     select_age = self.driver.find_element_by_xpath('//option[@value="{}"]'.format(randint(1930, 2004)))
    #     select_age.click()

    def add_my_name_to_petition(self):
        """
        Some of the times in some petition "add my name to petition" button appear before we can sign up
        to the petition, this function click on this button.
        REMOVE THIS FUNCTION WHEN THE A/B TEST IS DONE.
        """
        try:
            button = self.driver.find_element_by_css_selector('div.add-me-to-petition-button a.fl-button')
            button.click()
        except:
            print('Add my name to petition button not found, this button appear sometimes because its A/B test')
