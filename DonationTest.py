import random
import unittest

from selenium import webdriver


# TODO - do we want to check elements outside of the form? for instance, above the amount buttons
class Page:
    def __init__(self, site_url, expected_monthy_checkbox_text, expected_donations_amount, expected_currency_symbol):
        self.site_url = site_url
        self.expected_monthy_checkbox_text = expected_monthy_checkbox_text
        self.expected_donations_amount = expected_donations_amount
        self.expected_currency_symbol = expected_currency_symbol


class DonationTest(unittest.TestCase):

    def setUp(self):
        random_num = random.randint(1, 11)
        print(random_num)
        if random_num <= 5:
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()

    def test_donation_form(self):
        pages = [Page("https://animals-now.org/donate/?group=test", "תרומה חודשית",  ["50","120", "200", "400"], "₪" ),
                 Page("https://animals-now.org/en/donate/?group=test", "Monthly Donation",  ["25","35", "50", "100"], "$" ),
                 Page("https://challenge22.com/donate/?group=test", "Monthly Donation",  ["25","35", "50", "100"], "$" ),
                 Page("https://challenge22.com/es/donate/?group=test", "Donación mensual",  ["25","35", "50", "100"], "$" )]
        driver = self.driver
        for page in pages:
            print(page.site_url)
            driver.get(page.site_url)
            self.verify_hok_label(page.expected_monthy_checkbox_text)
            self.verify_donation_buttons(page.expected_donations_amount, page.expected_currency_symbol)

    def verify_hok_label(self, expected_monthy_checkbox_text):
        print(expected_monthy_checkbox_text)
        driver = self.driver
        monthy_checkbox_text = driver.find_element_by_id("isHokLabel").text
        self.assertIn(expected_monthy_checkbox_text, monthy_checkbox_text)

    def verify_donation_buttons(self, expected_donations_amount, expected_currency_symbol):
        print(expected_donations_amount, expected_currency_symbol)
        driver = self.driver
        donationButtons = driver.find_elements_by_css_selector(
            "#donate-form-general > div > div > form > div.form-group.val-button-container > button.donate-val-button")

        for idx, btn in enumerate(donationButtons):
            donation_amount = btn.find_element_by_class_name("amount").text
            currency_symbol = btn.find_element_by_class_name("currency").text
            self.assertIn(expected_currency_symbol, currency_symbol)
            self.assertIn(expected_donations_amount[idx], donation_amount)


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()




