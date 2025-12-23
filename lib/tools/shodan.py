#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import sys

import thirdparty.shodan.exception as ShodanException
from thirdparty.shodan import Shodan

from ..utils.colors import bad, good, info, run, tab, warn
from .ispcheck import ISPCheck


def shodan(domain, conf):
    config = ConfigParser()
    config.read(conf)
    res = []
    getAPI = config.get('SHODAN', 'API_KEY')
    print(info + 'Enumerating data from: %s using Shodan.io' % domain)
    api_key = input(tab + warn + 'Please enter your shodan API: ') if getAPI == '' else getAPI
    if getAPI == '':
        question = input(tab + warn + 'Do you want to save your securitytrails credentials? [Y/n] ')
        if question in ["yes", "y", "Y", "ye", '']:
            config.set('SHODAN', 'API_KEY', api_key)
        with open(conf, 'w+') as configfile:
            config.write(configfile)
            configfile.close()
    try:
        shodan = Shodan(api_key)
        counts = shodan.count(query=domain, facets=['ip'])
        print(tab + warn + "Total Associated IPs Found:")
        [(print(tab*2 + good + ip['value']), res.append(ip['value'])) if (ISPCheck(ip['value']) is None)
         else print(tab * 2 + bad + ip['value'] + ISPCheck(ip['value'])) for ip in counts['facets']['ip']]
        return res
    except ShodanException.APITimeout as e:
        print(tab + bad + "API timeout: %s" % str(e))
        return []
    except ShodanException.APIError as e:
        error_str = str(e).lower()
        # Only ask to delete credentials for actual authentication errors
        if 'invalid api key' in error_str or 'unauthorized' in error_str or '401' in error_str:
            print(tab + bad + "Invalid Shodan API key: %s" % e)
            ans = input(tab + warn + "Do you want to delete your credentials? [y/N]: ")
            if ans.lower() in ["yes", "y", "ye"]:
                config.set('SHODAN', 'API_KEY', '')
                with open(conf, 'w+') as configfile:
                    config.write(configfile)
                print(tab + good + "Your credentials have been deleted")
        else:
            # Connection error, rate limit, or other API error - don't suggest deleting keys
            print(tab + bad + "Shodan API error: %s" % e)
        return []
    except Exception as e:
        # Generic connection errors (SSL, timeout, network issues)
        error_msg = str(e) if str(e) else type(e).__name__
        if 'ssl' in error_msg.lower() or 'handshake' in error_msg.lower():
            print(tab + bad + "SSL/TLS connection error with Shodan API")
        elif 'timeout' in error_msg.lower():
            print(tab + bad + "Connection timeout with Shodan API")
        elif 'connection' in error_msg.lower():
            print(tab + bad + "Unable to connect to Shodan API - check your internet connection")
        else:
            print(tab + bad + "Error: %s" % error_msg)
        return []
