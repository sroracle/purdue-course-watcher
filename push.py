#!/usr/bin/env python3
from configparser import ConfigParser
from os.path      import expanduser
from smtplib      import SMTP_SSL
from sys          import argv, exit, stdin


def fatal_unconfigured():
    print('Error: it appears push has not been configured.')
    print('Please copy push.py.ini to ~/.config and edit it.')
    exit(1)


def configure(location=expanduser('~/.config/push.py.ini')):
    ini = ConfigParser()
    ini.read(location)
    if 'Username' not in ini['Connection']:
        ini['Connection']['Username'] = ini['Mail']['From']
    return ini


def push(ini, content):
    with SMTP_SSL(ini['Connection']['Server']) as sock:
        sock.ehlo()
        sock.login(ini['Connection']['Username'], ini['Connection']['Password'])
        sock.sendmail(ini['Mail']['From'], ini['Mail']['To'], content)


if __name__ == '__main__':
    msg = argv[1:] or stdin.readlines()
    if not msg:
        print('Error: must provide message on standard input or as argument.')
        exit(2)
    msg = ''.join(msg)
    try:
        config = configure()
    except KeyError:
        fatal_unconfigured()

    push(config, msg)
