import re
import socket

from lib.utils.colors import R, W, Y, tab, warn
from thirdparty import requests
from thirdparty.bs4 import BeautifulSoup
from thirdparty import urllib3

urllib3.disable_warnings()

cloudlist = ['sucuri',
             'cloudflare',
             'incapsula']


def ISPCheck(domain):
    reg = re.compile(rf'(?i){"|".join(cloudlist)}')
    try:
        header = requests.get('http://' + domain, timeout=3, verify=False).headers.get('server', '').lower()
        if header and reg.search(header):
            return f' is protected by {Y}{header.capitalize()}{W}'
        return None
    except Exception:
        # Fallback: try to check via check-host.net
        try:
            req = requests.get(f'https://check-host.net/ip-info?host={domain}', timeout=5, verify=False).text
            UrlHTML = BeautifulSoup(req, "lxml")
            if UrlHTML.findAll('div', {'class': 'error'}):
                return None  # Cannot retrieve info, but don't block

            for parse in UrlHTML.findAll('tr', {'class': 'zebra'}):
                if 'Organization' in str(parse):
                    org = parse.get_text(strip=True).split('Organization')[1].lower()
                    if reg.search(org):
                        return f' is protected by {Y}{reg.match(org).group().capitalize()}{W}'
        except Exception:
            pass  # If check-host.net also fails, continue with port check

        # Final fallback: check ports
        ports = [80, 443]
        for port in ports:
            try:
                checker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                checker.settimeout(0.5)
                if checker.connect_ex((domain, port)) == 0:
                    checker.close()
                    return None  # Port is open, not protected
                checker.close()
            except Exception:
                pass
        
        return None  # Return None instead of error to allow processing to continue
