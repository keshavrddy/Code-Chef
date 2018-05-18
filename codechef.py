import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import ssl
from functools import wraps
from config import ConfigSectionMap

cfg = ConfigSectionMap('setup')
START = cfg['start']
END = cfg['end']
session = requests.Session()
retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504])
session.proxies = proxies
session.headers = headers
session.mount('https://', HTTPAdapter(max_retries=retries))


def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar
ssl.wrap_socket = sslwrap(ssl.wrap_socket)

output_file = open(cfg['output_file'], 'a', encoding='utf-8')
exception_urls_file = open(cfg['exception_url_file'], 'a', encoding='utf-8')


for i in range(START, END):
    try:
        url_request = session.get(cfg['request_url'].format(str(i)))
    except Exception as e:
        print(e)
        continue
    if url_request.status_code != 404:
        print(url_request.url)
        user_name = url_request.url.split('/')[-1]
        req = session.get('https://www.codechef.com/users/' + str(user_name))
        if req.status_code != 404:
            soup = BeautifulSoup(req.content, 'lxml')
            box = soup.find('ul', {'class': 'side-nav'})
            try:
                details = {x.find('label').text.strip(): x.find('span').text.strip() for x in box if x.find('label') != -1}
            except TypeError:
                continue
            details['url'] = cfg['target_url'] + str(user_name)
            print(details)
            file.write(details.__str__() + '\n')
        else:
            file1.write(url_request.url + '\n')
            continue
    else:
        file1.write(url_request.url + '\n')
        continue
