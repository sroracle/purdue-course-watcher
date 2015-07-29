#!/usr/bin/env python
from sys import stdin, exit
from smtplib import SMTP_SSL
from configparser import ConfigParser
endl = '\r\n'

def config(ini):
   rc = ConfigParser()
   rc.read(ini)
   if 'Username' not in rc['Connection']:
      rc['Connection']['Username'] = rc['Mail']['From']
   return rc

def push(msg, ini = '/etc/push.py.ini'):
   rc = config(ini)
   with SMTP_SSL(rc['Connection']['Server']) as sock:
      sock.ehlo()
      sock.login(rc['Connection']['Username'], rc['Connection']['Password'])
      sock.sendmail(rc['Mail']['From'], rc['Mail']['To'], msg)
      sock.close()

if __name__ == '__main__':
   stdin = stdin.readlines()
   if not stdin:
      print('Must provide message on standard input.')
      exit(1)
   msg = endl + endl + ''.join(stdin)
   push(msg)
