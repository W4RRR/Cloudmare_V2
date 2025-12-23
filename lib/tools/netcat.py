#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import socket

import thirdparty.requests as requests
import thirdparty.urllib3 as urllib3
from thirdparty.html_similarity import similarity

from ..utils.colors import bad, good, info, tab, warn
from ..utils.settings import config, quest, apply_delay, is_auto_force
from ..utils.http_client import create_session
from .dnslookup import DNSLookup
from .ispcheck import ISPCheck

urllib3.disable_warnings()


def simCheck(data, page, ip, domain):
    sim = similarity(data.text, page.text)
    if sim > config['response_similarity_threshold']:
        print(tab + good + 'The connection has %d%% similarity to: %s' % (round(100 * sim, 2), domain))
        print(tab + good + '%s is the real IP' % ip)
        # Auto-force mode: don't stop, continue with other tests
        if not is_auto_force():
            quest(question='\n' + warn + 'IP found. Do yo want to stop tests?',
                  doY='sys.exit()', doN="pass")
    else:
        print(tab + bad + 'The connect has %d%% similarity to: %s' % (round(100 * sim, 2), domain))
        print(tab + bad + "%s is not the IP" % ip)


def netcat(domain, host, ignoreRedir, userAgent, randomAgent, header, count):
    headers = dict(x.replace(' ', '').split(':') for x in header.split(',')) if header is not None else {}
    headers.update({'User-agent': random.choice(open("data/txt/random_agents.txt").readlines()
                                                ).rstrip("\n")}) if randomAgent is True else ''
    headers.update({'User-agent': userAgent}) if userAgent is not None else ''

    A = DNSLookup(domain, host)
    question = None
    session = create_session()  # Use modern TLS session
    try:
        ip = socket.gethostbyname(str(host)) if count == 0 else str(A)
        isCloud = ISPCheck(ip)
        if isCloud is not None:
            print(tab + warn + ip + isCloud)
            return
        print(info + 'Connecting %s using as Host Header: %s' % (ip, domain))
        count += 1
        apply_delay()
        page = session.get('http://' + domain, timeout=config['http_timeout_seconds'], verify=False)
        hncat = page.url.replace('http://', '').split('/')[0]
        headers.update(host=hncat)
        apply_delay()
        data = session.get('http://' + ip, headers=headers,
                            timeout=config['http_timeout_seconds'], allow_redirects=False, verify=False)
        if data.status_code in [301, 302]:
            print(tab + info + "%s redirects to: %s" % ('http://' + ip, data.headers['Location']))
            # Auto-force mode: automatically follow redirects
            if is_auto_force():
                question = True
            else:
                question = (ignoreRedir if ignoreRedir is not True
                            else quest(
                                question=f'{tab}{info}Do you want to redirect?',
                                doY='True',
                                doN='False',
                                **{'return': True}
                                )
                            )
            data = session.get(
                'http://' + ip,
                headers=headers,
                timeout=config['http_timeout_seconds'],
                allow_redirects=question, verify=False
            )
        if data.status_code == 200:
            count += 1
        else:
            print(tab + bad + 'Unexpected status code [%s] occurred at: %s' %
                  (data.status_code, data.url))
            # Auto-force mode: automatically continue without prompting
            if is_auto_force():
                print(tab + info + 'Auto-forcing connection...')
                question = True
            else:
                question = quest(
                    question=f'{tab}{warn}Do you want to force the connection anyway?',
                    doY='True',
                    doN='False',
                    **{'return': True}
                )
            if not question:
                print(f'{tab}{warn}The process cannot be completed')
                return

        simCheck(data, page, ip, domain)

    except Exception as e:
        if question in ['y', 'yes', 'ye']:
            print(tab + bad + 'Error while connecting to: %s' % data.headers['Location'])
            return
        # Show meaningful error message instead of None
        error_msg = str(e) if str(e) else type(e).__name__
        if hasattr(e, 'errno') and e.errno:
            if e.errno == -2:
                error_msg = "DNS resolution failed - Host not found"
            elif e.errno == 111:
                error_msg = "Connection refused"
            elif e.errno == 110:
                error_msg = "Connection timed out"
            else:
                error_msg = f"Connection error (errno: {e.errno})"
        print(tab + bad + error_msg)
