#!/usr/bin/env python3

'''
Cloudmare_V2 - CloudProxy & Reverse Proxy Bypass Tool - Enhanced Edition

Original Author: MrH0wl (2018-2019)
Redesigned by: .W4R (2025)

This version includes Python 3 compatibility fixes, automatic dependency
installation, and performance improvements.
'''

from __future__ import absolute_import

import os
import sys
import subprocess

from .colors import G, R, W, Y, bad, end, good, tab, warn

# Required external dependencies (installed via pip)
REQUIRED_DEPENDENCIES = [
    'lxml',
]

# enable VT100 emulation for coloR text output on windows platforms
if sys.platform.startswith('win'):
    import ctypes
    kernel32 = ctypes.WinDLL('kernel32')
    hStdOut = kernel32.GetStdHandle(-11)
    mode = ctypes.c_ulong()
    kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
    mode.value |= 4
    kernel32.SetConsoleMode(hStdOut, mode)


def install_dependencies(silent=False):
    """Automatically installs required dependencies if missing."""
    missing = []
    for dep in REQUIRED_DEPENDENCIES:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)
    
    if missing:
        if not silent:
            print(f'{warn}Installing required dependencies: {", ".join(missing)}...')
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install'] + missing + 
                ['-q', '--disable-pip-version-check'],
                stdout=subprocess.DEVNULL if silent else None,
                stderr=subprocess.DEVNULL if silent else None
            )
            if not silent:
                print(f'{tab}{good}Dependencies installed successfully!')
            return True
        except subprocess.CalledProcessError as e:
            if not silent:
                print(f'{tab}{bad}Failed to install dependencies: {e}')
                print(f'{tab}{warn}Try running: pip install {" ".join(missing)}')
            return False
    return True


# Automatically install dependencies when loading the module
install_dependencies()


import random
import time

config = {
    'http_timeout_seconds': 5,
    'response_similarity_threshold': 0.9,
    'delay_min': 0,
    'delay_max': 0,
    'auto_force': False  # Auto-force connections without prompts
}


def apply_delay():
    """Apply random delay between requests if configured."""
    if config['delay_min'] > 0 or config['delay_max'] > 0:
        delay = random.uniform(config['delay_min'], config['delay_max'])
        time.sleep(delay)


def set_delay(delay_str):
    """Parse delay string like '1.2-2.4' and set config values."""
    if delay_str:
        try:
            if '-' in delay_str:
                parts = delay_str.split('-')
                config['delay_min'] = float(parts[0])
                config['delay_max'] = float(parts[1])
            else:
                config['delay_min'] = float(delay_str)
                config['delay_max'] = float(delay_str)
            print(f"{warn}Random delay enabled: {config['delay_min']}-{config['delay_max']}s between requests")
        except ValueError:
            print(f"{bad}Invalid delay format. Use '1.2-2.4' or '1.5'")


def set_auto_force(enabled):
    """Enable or disable auto-force mode for unattended operation."""
    config['auto_force'] = enabled
    if enabled:
        print(f"{warn}Auto-force mode enabled: will auto-continue on unexpected status codes")


def is_auto_force():
    """Check if auto-force mode is enabled."""
    return config.get('auto_force', False)

# version (<major>.<minor>.<month>.<day>)
VERSION = '2.0.0'
DESCRIPTION = 'CloudProxy & Reverse Proxy Bypass Tool - Enhanced Edition'
ISSUES_PAGE = 'https://github.com/W4RRR/Cloudmare_V2/issues/new'
GIT_REPOSITORY = 'https://github.com/W4RRR/Cloudmare_V2.git'
GIT_PAGE = 'https://github.com/W4RRR/Cloudmare_V2'
ZIPBALL_PAGE = 'https://github.com/W4RRR/Cloudmare_V2/zipball/main'
YEAR = '2025'
NAME = 'Cloudmare_V2 '
AUTHOR_ORIGINAL = 'MrH0wl'
AUTHOR_V2 = '.W4R'
COPYRIGHT = 'By %s | Redesigned by %s | GPL v3.0' % (AUTHOR_ORIGINAL, AUTHOR_V2)
PLATFORM = os.name
IS_WIN = PLATFORM == 'nt'

answers = {
    'affirmative': ['y', 'yes', 'ok', 'okay', 'sure', 'yep', 'yeah', 'yup', 'ya', 'yeh', 'ye', 'y'],
    'negative': ['n', 'no', 'nope', 'nop', 'naw', 'na', 'nah', 'nay', 'n'],
}


# colorful banner
def logotype():
    print(Y + '''
   _____ _                 _                        __      _____  
  / ____| |               | |                       \\ \\    / /__ \\ 
 | |    | | ___  _   _  __| |_ __ ___   __ _ _ __ ___\\ \\  / /  ) |
 | |    | |/ _ \\| | | |/ _` | '_ ` _ \\ / _` | '__/ _ \\\\ \\/ /  / / 
 | |____| | (_) | |_| | (_| | | | | | | (_| | | |  __/ \\  /  / /_ 
  \\_____|_|\\___/ \\__,_|\\__,_|_| |_| |_|\\__,_|_|  \\___|  \\/  |____|''' + W + '[' + R + VERSION + W + ']' + '''
''' + G + DESCRIPTION + G + '\n' + Y + '=' * 62 + W + '\n')


BASIC_HELP = (
    'domain',
    'bruter',
    'randomAgent',
    'host',
    'outSub',
)


# osclear shortcut
def osclear():
    if IS_WIN:
        os.system('cls')
    elif 'linux' in PLATFORM:
        os.system('clear')
    else:
        print("{bad} Can't identify OS")
    logotype()
    print(Y + '\n~ Thanks for using this script! <3')
    sys.exit(1)


def executer(command, **kwargs):
    try:
        if 'return' in kwargs.keys() and kwargs['return'] is True:
            return eval(command)
        exec(command)
    except Exception as e:
        if 'printError' in kwargs.keys():
            print(tab+kwargs['printError'])
            return
        print(f'{tab}{bad}{e}')


# question shortcut
def quest(question, doY='sys.exit(0)', doN='sys.exit(1)', defaultAnswerFor='yes', **kwargs):
    default = ' [Y/n]' if defaultAnswerFor.lower() in answers['affirmative'] else ' [y/N]'
    question = input(f'{question}{default}').lower().strip()

    if defaultAnswerFor.lower() == 'yes':
        answers['affirmative'].append('')
    elif defaultAnswerFor.lower() == 'no':
        answers['negative'].append('')

    if question in answers['affirmative']:
        exe = executer(doY, **kwargs)

    elif question in answers['negative']:
        exe = executer(doN, **kwargs)

    return exe


# Import Checker and downloader
class CheckImports:
    def __init__(self, libList=[]):
        for lib in libList:
            try:
                exec(lib)
            except ImportError or ModuleNotFoundError as e:
                if lib == libList[0]:
                    logotype()
                self.__downloadLib(e.name)

    def __downloadLib(self, lib):
        printMsg = {
            'printSuccess': f'{tab}{good}{lib} module is installed!',
            'printError': f'{tab}{bad}{lib} module is not installed! Try to install it manually.',
        }
        msg = f'{warn}{R}{lib}{end} module is required. Do you want to install?'
        command = f'subprocess.check_call([sys.executable, \'-m\', \'pip\', \'install\', \'{lib}\', '
        command += '\'-q\', \'--disable-pip-version-check\'])'
        quest(question=msg, doY=f"import subprocess\n{command}\nprint(kwargs[\'printSuccess\'])",
              doN='continue', **printMsg)
