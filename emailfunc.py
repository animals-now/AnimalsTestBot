import base64
import email
import pickle
import os.path
import gspread
from os.path import exists
from sys import exit
from time import sleep
from apiclient import errors
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import auth
from pprint import pprint


service = ""
def two_emails(service, user_id, search_string): #tell how many emails we found for search in gmail
    try:
        search_id = service.users().messages().list(userId=user_id, q=search_string).execute()
        number_results = int(search_id['resultSizeEstimate'])

        if number_results == 2:
            return ("Succeed! Thanks email and Salesforce email received")

        else:
            return ("Failed - Found " + str(number_results) + " emails instead of 2")

    except (errors.HttpError, errors):
        return ('Damn!..., an error has occured... %s' % errors)


def search_messages(service, user_id, search_string): #give messages ids according to search
    try:
        search_id = service.users().messages().list(userId=user_id, q=search_string).execute()
        number_results = search_id['resultSizeEstimate']
        final_list = list()
        if number_results > 0:
            message_ids = search_id['messages']
            for ids in message_ids:
                final_list.append(ids['id'])
            return final_list
        else:
            print('Zero results for that search string, returning and empty list.')
            return ""

    except (errors.HttpError, errors):
        print('shit..., an error has occured... %s' % errors)


def get_message(service, user_id, msg_id): #return message body according to msg id

    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        return('Message snippet: %s' % message['snippet'])
#       return message
    except (errors.HttpError, errors):
       return('An error occurred: %s' % errors)


