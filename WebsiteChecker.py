import customFunc
import requests
from requests.exceptions import ConnectionError
import random
import time

# If you add website, also add it in the error_status.json that located in the server
fish = "https://fish.org.il/"
etgar = "https://etgar22.co.il/"
ch = "https://challenge22.com/"
animals = "https://animals-now.org/"
anonymous = "https://anonymous.org.il/"
veg = 'https://veg.co.il/'
live_act = 'https://liveact.org/'

site_list = [etgar, ch, animals, anonymous, veg, live_act, fish]
service = customFunc.auth.get_service_gmail()

header_list = [
 {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like '
                'Gecko) Chrome/28.0.1464.0 Safari/537.36'},
 {'User-Agent': 'Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 '
                'Firefox/63.0'},
 {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like '
                'Gecko) Chrome/41.0.2228.0 Safari/537.36'},
 {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36'},
 {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 '
                'Firefox/5.0 Opera 11.11'},
 {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; '
                'Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)'},
 {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.59.12) '
                'Gecko/20160044 Firefox/52.59.12'},
 {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'},
 {'User-Agent': 'Mozilla/5.0 (X11;  Ubuntu; Linux i686; rv:52.0) '
                'Gecko/20100101 Firefox/52.0'},
 {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like '
                'Gecko) Chrome/35.0.2309.372 Safari/537.36'},
 {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, '
                'like Gecko) Chrome/33.0.1750.517 Safari/537.36'}]

header = random.choice(header_list)
for site in site_list:
    # First test, send get request if get error or the srv take more then 30 second to response - Fail
    start = time.time()
    try:
        request = requests.get(site, headers=header)
        if request.status_code == 200:
            customFunc.emailfunc.reset_error_counter('CodeError', service, site)
        else:
            customFunc.emailfunc.web_error_email('CodeError', service, str(request.status_code), site, str(header))
            continue
        customFunc.emailfunc.reset_error_counter('ConnectionError', service, site)
    except ConnectionError:
                customFunc.emailfunc.web_error_email('ConnectionError', service,
                                             'get request sent but the website does not respond', site, str(header))
        continue
    end = time.time()

    if end - start > 30:
        error = 'too much time to load - : ' + str(end - start)[0:4] + ' seconds'
        customFunc.emailfunc.web_error_email('LoadTimeError', service, error, site, str(header))
    else:
        customFunc.emailfunc.reset_error_counter('LoadTimeError', service, site)    
    customFunc.sleep(5)
    
    page = request.text  # get the page source code

    # Second test search for familiar words in the page, if not found - Fail.
    if 'animals' not in page:
         customFunc.emailfunc.web_error_email('FamiliarWordError', service,
                                             'The word "animals" does not found in the page source', site, str(header))
    else:
         customFunc.emailfunc.reset_error_counter('FamiliarWordError', service, site) 
    # Third test search for character that always appear in gibberish text, if found - Fail
    if '×' in page:
        customFunc.emailfunc.web_error_email('GibberishError', service,
                                             'Gibberish character("×") found in the page', site, str(header))
    else:
         customFunc.emailfunc.reset_error_counter('GibberishError', service, site)
