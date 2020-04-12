# AnimalsTestBot

Etgar22 and Challenge22 contain bots that sign up, check if the registration transfered to the correct sheet and send the result to another sheet called "Report".
PetitionsTest contain bot that sign up to all petitions and check if the user got thanks email and if the user info transfered to salesforce.
for every sign up saleforce got from test+???@animals-now.org it send email to our test email, so thats how the bot know if the sign up transfered to salesfoce or not.

auth.py - contain function create authorizations for google spreadsheets API and for gmail API.
token.pickle - gmail API authorization #result of auth
emailfunc.py - contain function to interact  with gmail API.
Etgar22FormTest.py - Etgar22 bot
Challenge22FormTest.py - Challenge22 bot
PetitionsTest.py - Petitions bot

creds.json, token.pickle and auth not found in git.
