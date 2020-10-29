import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import customFunc


# TODO - do we want to check elements outside of the form? for instance, above the amount buttons
class Page:
    def __init__(self, site_url, expected_monthy_checkbox_text, expected_donations_amount, expected_currency_symbol,
                 expected_label_name, expected_label_phone, expected_label_email):
        self.site_url = site_url
        self.expected_monthy_checkbox_text = expected_monthy_checkbox_text
        self.expected_donations_amount = expected_donations_amount
        self.expected_currency_symbol = expected_currency_symbol
        self.expected_label_name = expected_label_name
        self.expected_label_phone = expected_label_phone
        self.expected_label_email = expected_label_email


class DonationTest(unittest.TestCase):

    def setUp(self):
        session = customFunc.webFunc('no-site')
        session.start_driver()
        self.driver = session.driver

    def tearDown(self):
        self.driver.quit()

    def test_donation_form(self):
        params = "?group=test&utm_source=test&utm_medium=test&utm_campaign=test"
        pages = [
            Page("https://animals-now.org/donate/" + params, "תרומה חודשית", ["50", "120", "200", "400"], "₪",
                 "שם מלא:", "טלפון:", "אימייל:"),
            Page("https://animals-now.org/en/donate/" + params, 'Monthly Donation', ["25", "35", "50", "100"], "$",
                 'Full Name', 'Phone Number', 'Email Address'),
            Page("https://challenge22.com/donate/" + params, 'Monthly Donation', ["25", "35", "50", "100"], "$",
                 'Full Name', 'Phone Number', 'Email Address'),
            Page("https://challenge22.com/es/donate/" + params, "Donación mensual", ["25", "35", "50", "100"], "$",
                 'Nombre completo', "Numero de telefono", 'Email')
        ]
        driver = self.driver
        for page in pages:
            print(page.site_url)
            driver.get(page.site_url)
            self.close_popup(page.site_url)
            self.verify_hok_label(page.expected_monthy_checkbox_text)
            self.verify_donation_buttons(page.expected_donations_amount, page.expected_currency_symbol)
            self.go_to_2nd_page()
            self.verify_texts_on_2nd_page(page.expected_label_name, page.expected_label_phone,
                                          page.expected_label_email)

    def locate_popup(self, popup):
        driver = self.driver
        try:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, popup)))
            print("popup found")
            return True
        except BaseException:
            print("no popup")
            return False

    def close_popup(self, url):
        if not url.startswith('https://animals-now.org/donate'):
            print("No popup on this site")
            return

        driver = self.driver
        popup_css = "#popup-for-double-donation-round-light-version"
        close_btn_css = popup_css+" > .mfp-close"
        popup_exists = self.locate_popup(popup_css)

        if popup_exists:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,close_btn_css)))
            close_btn = driver.find_element_by_css_selector(close_btn_css)
            close_btn.click()

    def verify_hok_label(self, expected_monthy_checkbox_text):
        driver = self.driver
        monthy_checkbox_text = driver.find_element_by_id("isHokLabel").text
        self.assertIn(expected_monthy_checkbox_text, monthy_checkbox_text)

    def verify_donation_buttons(self, expected_donations_amount, expected_currency_symbol):
        driver = self.driver
        donation_buttons = driver.find_elements_by_css_selector(
            "#donate-form-general > div > div > form > div.form-group.val-button-container > button.donate-val-button")

        for idx, btn in enumerate(donation_buttons):
            donation_amount = btn.find_element_by_class_name("amount").text
            currency_symbol = btn.find_element_by_class_name("currency").text
            self.assertIn(expected_currency_symbol, currency_symbol)
            self.assertIn(expected_donations_amount[idx], donation_amount)

    def go_to_2nd_page(self):
        driver = self.driver
        submit_btn = driver.find_element_by_class_name('fl-button-submit')
        submit_btn.click()
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#padwrap > div.logo")))

    def verify_texts_on_2nd_page(self, expected_label_name, expected_label_phone,
                                 expected_label_email):
        driver = self.driver
        form = driver.find_element_by_css_selector("#padwrap > div.blockDetails.paymentDetails > div.blockDetailsIn")
        label_name = form.find_element_by_css_selector("div:nth-child(1) > label").text
        label_phone = form.find_element_by_css_selector("div:nth-child(2) > label").text
        label_email = form.find_element_by_css_selector("div:nth-child(3) > label").text

        self.assertIn(expected_label_name, label_name)
        self.assertIn(expected_label_phone, label_phone)
        self.assertIn(expected_label_email, label_email)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
