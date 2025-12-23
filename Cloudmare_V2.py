#!/usr/bin/env python3
# coding: utf-8
'''
Cloudmare_V2 - CloudProxy & Reverse Proxy Bypass Tool - Enhanced Edition

Original Author: MrH0wl (2018-2019)
Redesigned by: .W4R (2025)

https://github.com/W4RRR/Cloudmare_V2
'''

# default imports
import re
import signal

import socket

from lib import (DNSLookup, IPscan, censys, logotype, nameserver, netcat,
                 parser_cmd, quest, scan, securitytrails, shodan, sublist3r)
from lib.tools import ISPCheck
from lib.utils.colors import bad, warn, good, info, tab, G, R, Y, W
from lib.utils.settings import set_delay, apply_delay
from lib.utils.results import init_results, get_results, add_result
from thirdparty import urllib3

urllib3.disable_warnings()
verify = False


def keyboard_exit(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)

    quest(f"{warn}Do you want to clear the screen?", doY='osclear()', defaultAnswerFor='no')

    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, keyboard_exit)


if __name__ == "__main__":
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, keyboard_exit)
    args, parsErr = parser_cmd()
    output = "data/output/subdomains-from-" + (args.domain).split('.')[0] + ".txt" if args.outSub is None else False

    # Configure delay between requests if specified
    if args.delay:
        set_delay(args.delay)

    urlReg = re.compile(r'^(?:https?://)?(?:(?:w{2,3}\d{1})+|mobile\.|m(?:\d?)+\.)?((?:[.\w\d-]+))')
    args.domain = urlReg.search(args.domain).group(1)
    
    # Initialize results collector
    results = init_results(args.domain)
    
    subdomain = sublist3r.main(args.domain, args.threads, output, ports=None,
                               silent=False, verbose=args.verbose,
                               enable_bruteforce=args.subbrute, engines=None) if not args.disableSub else []

    if len(subdomain) == 0 and not any((
            args.host,
            args.brute,
            args.subbrute,
            args.censys,
            args.shodan,
            args.securitytrails
    )
    ):
        logotype()
        parsErr("cannot continue with tasks. Add another argument to task (e.g. \"--host\", \"--bruter\")")
    if args.headers is not None and 'host:' in args.headers:
        logotype()
        parsErr("Remove the 'host:' header from the '--header' argument. Instead use '--host' argument")

    if args.host is not None:
        check = ISPCheck(args.host)
        subdomain.append(args.host) if check is None else print(f"{bad}{args.host}{check}")

    if args.brute is True:
        nameservers = nameserver(args.domain)
        subdomain.extend(nameservers)

    if args.censys is not None:
        CensysIP = censys(args.domain, args.censys)
        subdomain.extend(CensysIP)

    if args.shodan is not None:
        ShodanIP = shodan(args.domain, args.shodan)
        subdomain.extend(ShodanIP)

    if args.securitytrails is not None:
        STip = securitytrails(args.domain, args.securitytrails)
        subdomain.extend(STip)

    list_length = len(subdomain)
    for i in range(list_length):
        host = subdomain[i]
        
        # Check if host is protected by WAF and collect results
        try:
            ip = socket.gethostbyname(str(host))
            waf_check = ISPCheck(host)
            
            if waf_check is not None:
                # Extract WAF provider from the check result
                waf_provider = None
                for provider in ['cloudflare', 'sucuri', 'incapsula']:
                    if provider in waf_check.lower():
                        waf_provider = provider.capitalize()
                        break
                
                # This is a WAF-protected IP
                add_result(
                    subdomain=host,
                    waf_ip=ip,
                    waf_provider=waf_provider,
                    status='protected'
                )
            else:
                # This could be a real IP (not behind WAF)
                add_result(
                    subdomain=host,
                    real_ip=ip,
                    status='exposed'
                )
        except socket.gaierror:
            # DNS resolution failed
            add_result(
                subdomain=host,
                status='error'
            )
        except Exception:
            add_result(
                subdomain=host,
                status='error'
            )
        
        scan(args.domain, host, args.uagent, args.randomAgent, args.headers)
        netcat(args.domain, host, args.ignoreRedirects, args.uagent, args.randomAgent, args.headers, count=0)
        A = DNSLookup(args.domain, host)
        IPscan(args.domain, host, A, args.uagent, args.randomAgent, args.headers, args)
    
    # Print and save results
    results.print_summary()
    
    if args.outResults:
        base_path = f"data/output/results-{args.domain.split('.')[0]}"
        if args.outResults == 'all':
            results.save(base_path, formats=['json', 'csv', 'txt'])
        else:
            # Parse comma-separated formats
            formats = [f.strip().lower() for f in args.outResults.split(',')]
            results.save(base_path, formats=formats)

