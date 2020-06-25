import base64
from email.mime.text import MIMEText
from apiclient import errors
import json


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


def signup_failed_email(service, row):
    message_text = "Sheet\Petition: " + row[1] + " Email: " + row[2] + " Reason: " + row[3]
    sender = "me"
    subject = "Sign Up Failed"
    to_list = ["maor@animals-now.org", "dev@animals-now.org"]
    user_id = "me"

    for to in to_list:
        message = create_message(sender, to, subject, message_text)
        send_message(service, user_id, message)


def petition_emails(service, user_id, search_string):  # tell how many emails we found for search in gmail
    try:
        search_id = service.users().messages().list(userId=user_id, q=search_string).execute()
        number_results = int(search_id['resultSizeEstimate'])

        if number_results == 1:
            return "Succeed! Salesforce email received"

        else:
            return "Failed - Found " + str(number_results) + " emails instead of 1"

    except (errors.HttpError, errors):
        return 'Damn!..., an error has occured... %s' % errors
    
def web_error_email_no_delay(service, error, site, header):
    message_text = "Error: " + error + ", Website: " + site + ", header: " + header
    sender = "me"
    subject = "WebSite Error"
    to_list = ["maor@animals-now.org", "dev@animals-now.org"]
    user_id = "me"

    for to in to_list:
        message = create_message(sender, to, subject, message_text)
        send_message(service, user_id, message)
 

# Check if email already sent in the last five sessions. if email already sent, email will not send again.
# the code open json file, the json file contain site and dict of error for each site. the error dict contain error and counter(type=INT) like that: "SomeError": counter
# the counter indicate when the last failure email sent, counter = 5 mean that in was sent in the last session and counter = 0 mean that the last email sent before more than
# 5 sessions
json_path = '/home/maor_animals_now_org/pytest/error_status.json'
def web_error_email(error_type, service, error, site, header):
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        f.close()

        if data[site][error_type] == 0:
            web_error_email_no_delay(service, str(error), site, str(header))
            data[site][error_type] = 5
            with open(json_path, 'w+') as f:
                f.write(json.dumps(data))
            f.close()
        else:
            data[site][error_type] = data[site][error_type] - 1
            with open(json_path, 'w+') as f:
                f.write(json.dumps(data))
            f.close()
    except: # if there is trouble with the json file, the email will sent every session
        web_error_email_no_delay(service, (str(error) + ". Also JSON file failed - no delay between emails(code problem)"), site, str(header))
     
def reset_error_counter(error_type, service, site):
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        f.close()
        if data[site][error_type] != 0:
            data[site][error_type] = 0
            with open(json_path, 'w+') as f:
                 f.write(json.dumps(data))
            f.close()
    except:
        web_error_email_no_delay(service, ("fail to reset error counter: " + error_type), site, 'irelevant')   
