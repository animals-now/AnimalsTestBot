import unittest
import customFunc
from customFunc import gmail_checker, log_date
from DonationTest import close_popup
from time import sleep
from selenium.common.exceptions import NoSuchElementException


class DonationTest(unittest.TestCase):

    url_list = {
        "turkey": "https://animals-now.org/investigations/turkey/?utm_source=test&utm_medium=test&utm_campaign=test",
        "live_transports": "https://animals-now.org/issues/live-transports/?utm_source=test&utm_medium=test&utm_campaign=test",
        "cages": "https://animals-now.org/issues/cages/?utm_source=test&utm_medium=test&utm_campaign=test",
        "protection_act": "https://animals-now.org/issues/animal-protection-act/?utm_source=test&utm_medium=test&utm_campaign=test",
        "fish": "https://animals-now.org/investigations/fish/?utm_source=test&utm_medium=test&utm_campaign=test",
        "zoglobek": "https://animals-now.org/issues/zoglobek-lawsuit/?utm_source=test&utm_medium=test&utm_campaign=test",
        "fur": "https://animals-now.org/issues/fur/?utm_source=test&utm_medium=test&utm_campaign=test",
        "stop_cages": "https://animals-now.org/issues/stop-cages/?utm_source=test&utm_medium=test&utm_campaign=test",
        #"september_2020": "https://animals-now.org/investigations/investigation-september-2020/?utm_source=test&utm_medium=test&utm_campaign=test",
    }

    def test_signing(self):
        """
        When petition registration success, the user's details transfer to salesforce. if salesforce receive
        email with this form: test+???@animals-now.org, salesforce will send the user details to test@animals-now.org.
        This function search in test@animals-now.org inbox for email from saleforce
        with the user's details, if the email not found the test failed
        """
        results = [] # list with (email used to signed up,petition_name,petition_url)
        failed = [] # list of failed signups
        for petition_name in self.url_list: # sign up to petitions in the site list, for each sign up generate new info
            try:
                petition_url = self.url_list[petition_name]
                result = self.sign(petition_name, petition_url, 6, 3)
                results.append(result)
            except NoSuchElementException:
                failed.append(log_date() + petition_name + ": element not found. " + petition_url)
            except Exception as Err:
                failed.append(log_date() + petition_name + ": " + str(Err) + " " + petition_url)

        first_email = next(iter(results[0]))

        session = customFunc.webFunc('None')
        gmail = gmail_checker()

        # wait up to 150 seconds for the first email to arrive, try every 10 seconds
        max_time = 150  # seconds
        try_time = 10  # seconds
        sleep(try_time)
        while max_wait > 0 and num_emails_received < 1:
            max_wait = max_wait - try_time
            sleep(try_time)
            num_emails_received = gmail.count(first_email, 'me')

        # test all emails
        for result in results:
            (email_address, petition_name, petition_url) = result
            num_emails_received = gmail.count(email_address, 'me')
            if num_emails_received != 1:
                failed.append(log_date() + petition_name + " emails received: " + str(num_emails_received) + " link " + petition_url)

        self.assertFalse(failed)

    def sign(self, petition_name, url, wait_before, wait_after):
        session = customFunc.webFunc(url)
        session.start_driver()
        session.url()
        close_popup(session.driver, url)
        sleep(wait_before)
        # print('petition name: "{}" url: "{}"'.format(petition_name,url))
        session.add_my_name_to_petition()  # DELETE WHEN A/B THE IS DONE
        sleep(wait_after)
        session.insert_info_to_field('FirstName', session.first_name)
        session.insert_info_to_field('LastName', session.last_name)
        session.insert_info_to_field('Email', session.email)
        session.insert_info_to_field('Phone', session.phone)
        session.petitions_send()
        email = session.email
        session.driver.quit()
        return (email, petition_name, url)
