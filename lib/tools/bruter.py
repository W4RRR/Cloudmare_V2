#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

import thirdparty.requests as requests
import thirdparty.urllib3 as urllib3
from lib.tools.ispcheck import ISPCheck
from thirdparty.dns import resolver

urllib3.disable_warnings()

from ..utils.colors import W, Y, bad, good, info, tab, warn
from ..utils.settings import config
from ..utils.http_client import create_session


def donames_list():
    donames = []
    file_ = "/data/txt/domains.txt"
    path = os.getcwd()+file_
    with open(path, 'r') as f:
        domlist = [line.strip() for line in f]
        for item in domlist:
            donames.append(item)
    return donames


def bruter(domain):
    good_check = []
    donames = donames_list()
    url = 'http://' + domain
    session = create_session()  # Use modern TLS session
    try:
        page = session.get(url, timeout=config['http_timeout_seconds'], verify=False)
        http = 'http://' if 'http://' in page.url else 'https://'
        host = page.url.replace(http, '').split('/')[0]
        webname = host.split('.')[1].replace('.', '') if 'www' in host else host.split('.')[0]
        for i in donames:
            domain = webname + i if '.' not in webname else webname.split(0)
            if url.replace('http://', '') not in domain:
                good_check.append(domain)
        return good_check
    except requests.exceptions.SSLError:
        print("   " + bad + 'Error handshaking with SSL')
        return []
    except requests.exceptions.ReadTimeout:
        print("   " + bad + "Connection Timeout")
        return []
    except requests.ConnectTimeout:
        print("   " + bad + "Connection Timeout ")
        return []
    except Exception as e:
        print("   " + bad + f"Connection error: {e}")
        return []


def nameserver(domain):
    rdtypes = ['MX', 'NS']
    regex = re.compile(r'([-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b)[-a-zA-Z0-9()@:%_\+.~\#\?&\/=]*$')
    checking = bruter(domain)
    good_dns = []
    print(info + 'Bruteforcing domain extensions and getting DNS records')
    if not checking:
        print(tab + warn + f'No domain extensions to check')
        return good_dns
    print(tab + warn + f'Total domain extension used: {Y}{len(checking)}{W}')
    for item in checking:
        try:
            for rdtype in rdtypes:
                retrived = resolver.query(item, rdtype)
                for data in retrived:
                    data = regex.search(data.to_text()).group(1)
                    isCloud = ISPCheck(data)
                    if isCloud is None:
                        if data not in good_dns:
                            good_dns.append(data)
                            print(tab*2 + good + f'{rdtype} Record: ' + str(data) + ' from: ' + item)
                        continue
                    print(tab*2 + bad + f'{rdtype} Record: ' + str(data) + ' from: ' + item + isCloud)
        except Exception as e:
            if (type(e).__name__ == 'NXDOMAIN'):
                err = str(e).split(':')[0]
                print(tab*2 + bad + f'{err}: {Y+item+W}')
                continue
            print(e)
    return good_dns
