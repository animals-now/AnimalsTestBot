# AnimalsTestBot

Etgar22 and Challenge22 contain bots that sign up, check if the registration transfered to the correct sheet and send the result to another sheet called "Report".

PetitionsTest contain bot that sign up to all petitions and check if the user info transfered to salesforce.
for every sign up saleforce got from test+???@animals-now.org it send email to our test email, so thats how the bot know if the sign up transfered to salesfoce or not.

WebsiteChecker send get request to our websites(see which websites in the websitecheker.py) if get error or the website doesn't respond for more than 15 second the test fail. also check if the websites contain any gibrrish char and if the websites contain words that must appear in any of our websites. if gibbrish char found in the website or if any of the words doesn't appear in the website the test fail.

*For every failure email send to dev with data about the failure.

auth.py - contain function that create authorizations for google spreadsheets API and for gmail API

token.pickle - gmail API authorization  # result of auth

emailfunc.py - contain function to interact  with gmail API
