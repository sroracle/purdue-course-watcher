#!/usr/bin/env python3
from argparse import ArgumentParser
from http.client import HTTPSConnection
from os.path import expanduser
from sys import path
# XXX external
from bs4 import BeautifulSoup
# XXX internal
import push


readline = ArgumentParser(description = 'Lookup seat availability for a course '
                          'in myPurdue.')
readline.add_argument('-p', '--push', action = 'store_true', help = 'Send '
                             'notification to configured mobile device. The '
                             'file ~/.config/push.py.ini must be configured.')
readline.add_argument('term', type = int, help = 'School semester. For example, '
                      '201610 is Fall 2015 (take careful note that it uses the '
                      'wrong year for fall terms), and 201620 is Spring 2016.')
readline.add_argument('crn', metavar = 'CRN', type = int, help = 'Course '
                      'request number.')
args = readline.parse_args()


domain = 'selfservice.mypurdue.purdue.edu'
path = '/prod/bwckschd.p_disp_detail_sched?term_in=%s&crn_in=%s' % (args.term,
       args.crn)
sock = HTTPSConnection(domain)
sock.request('GET', path)
try:
   html = sock.getresponse().read()
   html = html.decode()
except:
   print('Error connecting to myPurdue:')
   raise


try:
   soup = BeautifulSoup(html)
   seats = int(soup.select('table.datadisplaytable td.dddefault')[3].get_text())
   wl = int(soup.select('table.datadisplaytable td.dddefault')[5].get_text())
   course = soup.select('table.datadisplaytable th')[0].get_text()
except:
   print('Error parsing myPurdue output:')
   raise


if seats > 0 and wl <= 0:
   result = 'There are %s open seats in %s!' % (seats, course)
   print(result)
   if args.push:
      try: rc = push.config()
      except KeyError: push.fatal_unconfigured()
      push.push(rc, 'Purdue course watcher\n' + result)
