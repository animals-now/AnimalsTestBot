import customFunc
import requests
from requests.exceptions import ConnectionError
import time

etgar = "https://etgar22.co.il/?utm_source=test&utm_medium=test&utm_campaign=test"
ch = "https://challenge22.com/?utm_source=test&utm_medium=test&utm_campaign=test"
ch_es = "https://challenge22.com/es/?utm_source=test&utm_medium=test&utm_campaign=test"
animals = "https://animals-now.org/?utm_source=test&utm_medium=test&utm_campaign=test"
anonymous = "https://anonymous.org.il/?utm_source=test&utm_medium=test&utm_campaign=test"
veg = 'https://veg.co.il/?utm_source=test&utm_medium=test&utm_campaign=test'

site_list = [etgar, ch, ch_es, animals, anonymous, veg]

for site in site_list:
    start = time.time()
    try:
        request = requests.get(site)
        if request.status_code == 200:
            pass
        else:
            customFunc.emailfunc.web_error_email(service, str(request.status_code), site)

    except ConnectionError:
        customFunc.emailfunc.web_error_email(service, 'Web site does not exist', site)
    end = time.time()

    if end - start > 15:
        error = 'to much time to load - : ' + str(end - start)[0:4] + ' seconds'
        customFunc.emailfunc.web_error_email(service, error, site)
    customFunc.sleep(10)


