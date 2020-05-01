import base64
from email.mime.text import MIMEText
from apiclient import errors


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


def send_emails(service, row):
    message_text = "Sheet\Petition: " + row[1] + " Email: " + row[2] + " Reason: " + row[3]
    sender = "me"
    subject = "Sign Up Failed"
    to_list = ["maor@animals-now.org", ]
    user_id = "me"

    for to in to_list:
        message = create_message(sender, to, subject, message_text)
        send_message(service, user_id, message)


def two_emails(service, user_id, search_string):  # tell how many emails we found for search in gmail
    try:
        search_id = service.users().messages().list(userId=user_id, q=search_string).execute()
        number_results = int(search_id['resultSizeEstimate'])

        if number_results == 2:
            return "Succeed! Thanks email and Salesforce email received"

        else:
            return "Failed - Found " + str(number_results) + " emails instead of 2"

    except (errors.HttpError, errors):
        return 'Damn!..., an error has occured... %s' % errors
