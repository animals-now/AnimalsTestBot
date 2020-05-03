import customFunc
#import requests
from requests.exceptions import ConnectionError
import random
import time

etgar = "https://etgar22.co.il/?utm_source=test&utm_medium=test&utm_campaign=test"
ch = "https://challenge22.com/?utm_source=test&utm_medium=test&utm_campaign=test"
ch_es = "https://challenge22.com/es/?utm_source=test&utm_medium=test&utm_campaign=test"
animals = "https://animals-now.org/?utm_source=test&utm_medium=test&utm_campaign=test"
anonymous = "https://anonymous.org.il/?utm_source=test&utm_medium=test&utm_campaign=test"
veg = 'https://veg.co.il/?utm_source=test&utm_medium=test&utm_campaign=test'

site_list = [etgar, ch, ch_es, animals, anonymous, veg]
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
    start = time.time()
    try:
        request = requests.get(site, headers=header)
        if request.status_code == 200:
            pass
        else:
            customFunc.emailfunc.web_error_email(service, str(request.status_code),site ,str(header))

    except ConnectionError:
        customFunc.emailfunc.web_error_email(service, 'Web site does not exist', site, str(header))
    end = time.time()

    if end - start > 15:
        error = 'to much time to load - : ' + str(end - start)[0:4] + ' seconds'
        customFunc.emailfunc.web_error_email(service, error, site, str(header))
    customFunc.sleep(10)

