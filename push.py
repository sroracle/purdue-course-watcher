#!/usr/bin/env python3
from configparser import ConfigParser
from os.path import expanduser
from smtplib import SMTP_SSL
from sys import argv, exit, stdin


def fatal_unconfigured():
   print('Error: it appears push has not been configured.')
   print('Please copy push.py.ini to ~/.config and edit it.')
   exit(1)


def config(ini = expanduser('~/.config/push.py.ini')):
   rc = ConfigParser()
   rc.read(ini)
   if not rc.sections(): raise KeyError
   if 'Username' not in rc['Connection']:
      rc['Connection']['Username'] = rc['Mail']['From']
   return rc


def push(rc, msg):
   with SMTP_SSL(rc['Connection']['Server']) as sock:
      sock.ehlo()
      sock.login(rc['Connection']['Username'], rc['Connection']['Password'])
      sock.sendmail(rc['Mail']['From'], rc['Mail']['To'], msg)
      sock.close()


if __name__ == '__main__':
   msg = argv[1:] or stdin.readlines()
   if not msg:
      print('Error: must provide message on standard input or as an argument.')
      exit(2)
   msg = ''.join(msg)
   try: rc = config()
   except KeyError: fatal_unconfigured()
   push(rc, msg)
