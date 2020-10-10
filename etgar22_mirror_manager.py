import requests
from requests.exceptions import ConnectionError
import random
import time
import json
import base64
from email.mime.text import MIMEText
from apiclient import errors
import auth

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

gmail_service = auth.get_service_gmail()

def create_message(sender, to, subject, message_text):
    """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_message(service, user_id, message):
    """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
    try:
        (service.users().messages().send(userId=user_id, body=message).execute())
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
  
def send_email(sender, to, subject, message_text):
    message = create_message(sender, to, subject, message_text)
    send_message(gmail_service, "me", message)
    print(subject + ": " + message_text)

def read_file(filename):
    offset = -1
    maxlen = -1
    fp = open(filename,'rb')
    ret = False
    try:
        if (offset > 0):
            fp.seek(offset)
        ret = fp.read(maxlen)
        return ret
    finally:
        fp.close( )
    
    return ret

local_test = 0
test = 1
production = 2

# operation_mode = local_test
# operation_mode = test
operation_mode = production


#test_mode = True
#localhost_most = True


send_notification_emails_to = "oded@animals-now.org"
send_notification_emails_from = "test@animals-now.org"


if operation_mode == local_test:
    host_to_check = "localhost"
    # etgar22_url = "https://test.etgar22.co.il/"
    do_mirror_url = "https://localhost/monitor.etgar22.co.il/mirror_etgar22_test.php"
    etgar22_original_ip_url = 'https://127.0.0.1/test.etgar22.co.il/monitor.txt'
    seconds_to_wait_before_start_mirror = 10

elif operation_mode == test:
    host_to_check = "test.etgar22.co.il"
    # etgar22_url = "https://test.etgar22.co.il/"
    do_mirror_url = "https://monitor.etgar22.co.il/mirror_etgar22_test.php"
    etgar22_original_ip_url = 'https://80.179.230.68/monitor.txt'
    seconds_to_wait_before_start_mirror = 10

elif operation_mode == production:
    host_to_check = "etgar22.co.il"
    # etgar22_url = "https://etgar22.co.il/"
    do_mirror_url = "https://monitor.etgar22.co.il/mirror_etgar22.php"
    etgar22_original_ip_url = 'https://80.179.230.68/monitor.txt'
    seconds_to_wait_before_start_mirror = 120

state_path = '/home/oded_animals_now_org/pytest/etgar22_mirror_manager_state.json'
mirror_etgar22_code = read_file('/home/oded_animals_now_org/pytest/mirror_etgar22_code.txt')


# print(mirror_etgar22_code)

with open(state_path, 'r') as state_file:
    state = json.load(state_file)
state_file.close()

headers = { 'Host': host_to_check }

found_connection_error = False


try:
    request = requests.get(etgar22_original_ip_url, headers=headers, timeout=30, verify=False)
    

    if request.status_code == 200:

        if state["mirror_on"]:
            # then time to stop the mirror
            params_to_send = {
                    "code": mirror_etgar22_code,
                    "do_mirror": "0"
                }

            try:
                result_from_monitor = requests.post(do_mirror_url, data = params_to_send, verify=False)
                result_from_monitor = result_from_monitor.json()
                if "error" in result_from_monitor:
                    # send email that mirror_etgar22.php stop mirror return error
                    send_email(send_notification_emails_from, send_notification_emails_to, 
                        "Error when trying to stop mirror_etgar22", result_from_monitor["error"])
                else:
                    state["mirror_on"] = False
                    state["last_error_time"] = ""

                    send_email(send_notification_emails_from, send_notification_emails_to, 
                        "Successfully stopped mirror_etgar22", "Successfully stopped mirror_etgar22")


            except ConnectionError as err:
                    send_email(send_notification_emails_from, send_notification_emails_to, 
                            "Error when trying to stop mirror_etgar22", "Connection Error to: " + do_mirror_url + " - " + 
                            str(err))
        else:
            state["last_error_time"] = ""
            print('All is good!')
    else:
        found_connection_error = True
        connection_error_description = request.status_code
        print ("Can't connect to " + etgar22_original_ip_url + " - " + str(request.status_code) )



except ConnectionError as err:
    found_connection_error = True
    connection_error_description = "Connection Exception"
    print ("Can't connect to " + etgar22_original_ip_url + " - " + str(err))


if found_connection_error:

    state['last_error'] = connection_error_description

    if state["mirror_on"]:
        # do nothing, stay in mirror mode
        print ("Staying in mirror mode")
        pass
    else:
        last_error_time = state["last_error_time"];
        if last_error_time == '':
            #found an error, write the time
            state["last_error_time"] = time.time()
        else:
            seconds_since_last_error = time.time() - state["last_error_time"]

            # print ("Seconds since last error: " + str(seconds_since_last_error))

            if seconds_since_last_error > seconds_to_wait_before_start_mirror:
                #site is down for more then seconds_to_wait_before_start_mirror, try to start mirror mode!
                params_to_send = {
                    "code": mirror_etgar22_code,
                    "do_mirror": "1"
                }
                try:
                    result_from_monitor = requests.post(do_mirror_url, data = params_to_send, verify=False)
                    result_from_monitor = result_from_monitor.json()
                    if "error" in result_from_monitor:
                        send_email(send_notification_emails_from, send_notification_emails_to, 
                            "Error when trying to start mirror_etgar22", result_from_monitor["error"])

                    else:
                        state["mirror_on"] = True
                        send_email(send_notification_emails_from, send_notification_emails_to, 
                            "Successfully started mirror_etgar22", "Successfully started mirror_etgar22")

                except ConnectionError as err:
                    send_email(send_notification_emails_from, send_notification_emails_to, 
                            "Error when trying to start mirror_etgar22", "Connection Error to: " + do_mirror_url + " - " + 
                            str(err))
                    
with open(state_path, 'w') as state_file:
    json.dump(state, state_file)
