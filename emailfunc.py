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
    """
    Use to send email about failure to sign up for petition and challenges
    Accept:
    service - gmail api auth
    row - list that contain information about the failure
    """
    message_text = "Sheet\Petition: " + row[1] + "Link: " + row[2] + " Email: " + row[3] + " Reason: " + row[4]
    sender = "me"
    subject = "Sign Up Failed"
    to_list = ["dev@animals-now.org"]
    user_id = "me"

    for to in to_list:
        message = create_message(sender, to, subject, message_text)
        send_message(service, user_id, message)

def web_error_email_no_delay(service, error, site, header):
    """
    Sent failure email when website test fail.
    """
    message_text = "Error: " + error + ", Website: " + site + ", header: " + header
    sender = "me"
    subject = "WebSite Error"
    to_list = ["dev@animals-now.org"]
    user_id = "me"

    for to in to_list:
        message = create_message(sender, to, subject, message_text)
        send_message(service, user_id, message)
        
# this function here to send Roni email when veg fail,
#I know its stuipd and bad code to dublicate the function
# but I its the faster way to do that.
def veg_error_email_no_delay_roni(service, error, site, header):
    message_text = "Error: " + error + ", Website: " + site + ", header: " + header
    sender = "me"
    subject = "WebSite Error"
    to_list = ["roni@animals-now.org"]
    user_id = "me"
    for to in to_list:
        message = create_message(sender, to, subject, message_text)
        send_message(service, user_id, message)




json_path = '/home/maor_animals_now_org/pytest/error_status.json'
def web_error_email(error_type, service, error, site, header):
    """
    Check if email already sent in the last five sessions. if email already sent,
    email will not send again.
    the code open json file, the json file contain sites and dict of error for each site.
    the error dict contain error and counter(type=INT) like that: "SomeError": counter
    the counter indicate when the last failure email sent. counter = 5 mean failure email was sent
    in the last session, counter = 0 mean the last failure email sent before more than
    5 sessions
    """

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        f.close()

        if data[site][error_type] == 0:
            web_error_email_no_delay(service, str(error), site, str(header))
            #if the site is veg send to Roni also mail
            if 'veg' in site:
                veg_error_email_no_delay_roni(service, str(error), site, str(header))
            # session to wait between each email
            data[site][error_type] = 1
            with open(json_path, 'w+') as f:
                f.write(json.dumps(data))
            f.close()
        else:
            data[site][error_type] = data[site][error_type] - 1
            with open(json_path, 'w+') as f:
                f.write(json.dumps(data))
            f.close()
    except:  # if there is trouble with the json file, the email will sent every session
        web_error_email_no_delay(service,
                                 (str(error) + ". Also JSON file failed - no delay between emails(code problem)")
                                 , site, str(header))
                    #if the site is veg send to Roni also mail
        if 'veg' in site:
            veg_error_email_no_delay_roni(service, str(error), site, str(header))

def reset_error_counter(error_type, service, site):
    """
    Reset the json file error counter when test succeed, each time subtract one from the counter.
    """
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        f.close()
        if data[site][error_type] != 0:
            data[site][error_type] = data[site][error_type] - 1
            with open(json_path, 'w+') as f:
                f.write(json.dumps(data))
            f.close()
    except:
        web_error_email_no_delay(service, ("fail to reset error counter: " + error_type), site, 'irrelevant')
