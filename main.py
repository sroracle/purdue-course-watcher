#!/usr/bin/env python
from sys import path
from bs4 import BeautifulSoup as soup
from argparse import ArgumentParser as argparse
from http.client import HTTPSConnection as https

readline = argparse(description='Lookup seat availability for a course in myPurdue.')
try:
   path.append('/usr/local/bin')
   from push import push
   readline.add_argument('-p', '--push', action = 'store_true', help = 'Send'
                         'notification to configured mobile device.')
   canpush = True
except: canpush = False
readline.add_argument('term', type = int, help = 'School semester. For example, '
                      '201610 is Fall 2015 (take careful note that it uses the '
                      'wrong year for fall terms), and 201620 is Spring 2016.')
readline.add_argument('crn', metavar='CRN', type=int, help='Course request number.')
args = readline.parse_args()
if not canpush: args.push = False

domain = 'selfservice.mypurdue.purdue.edu'
path = '/prod/bwckschd.p_disp_detail_sched?term_in=%s&crn_in=%s' % (args.term, args.crn)
sock = https(domain)
sock.request('GET', path)
try:
   out = sock.getresponse().read()
   out = out.decode()
except:
   print('Error connecting to myPurdue:')
   raise

try:
   tree = soup(out)
   seats = int(tree.select('table.datadisplaytable td.dddefault')[2].get_text())
   course = tree.select('table.datadisplaytable th')[0].get_text()
except:
   print('Error parsing myPurdue output:')
   raise

if seats > 0:
   result = 'There are %s open seats in %s!' % (seats, course)
   print(result)
   if args.push:
      push('Purdue course watcher\n' + result)
