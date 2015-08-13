#!/usr/bin/env python3
from   argparse    import ArgumentParser
from   http.client import HTTPSConnection
# external
from   bs4         import BeautifulSoup
# internal
import push


class PuCourse:

    def __init__(self, term, crn):
        '''Creates a new PuCourse object based on the given term and CRN.'''
        self.term = term
        self.crn = crn
        self.domain = 'selfservice.mypurdue.purdue.edu'
        self.path = '/prod/bwckschd.p_disp_detail_sched?term_in=%s' \
                    '&crn_in=%s' % (self.term, self.crn)

    def scrape(self):
        '''Scrapes myPurdue for the course's information.'''
        sock = HTTPSConnection(self.domain)
        sock.request('GET', self.path)
        try:
            self.html = sock.getresponse().read()
            self.html = self.html.decode()
        except:
            print('Error connecting to myPurdue:')
            raise
        finally:
            sock.close()

    def parse(self):
        '''Parses the scrape for the course's information.'''
        try:
            soup = BeautifulSoup(self.html)
            data = soup.select('table.datadisplaytable td.dddefault')
            self.seats = int(data[3].get_text())
            self.waits = int(data[5].get_text())
            self.name = soup.select('table.datadisplaytable th')[0].get_text()
        except:
            print('Error parsing myPurdue output:')
            raise


def main():
    readline = ArgumentParser(description='Lookup seat availability for a'
                              ' course in myPurdue.')
    readline.add_argument('-p', '--push', action='store_true', help='Send'
                          ' a notification to your mobile device if a seat is'
                          ' available. The file ~/.config/push.py.ini must be'
                          ' configured.')
    readline.add_argument('term', metavar='<term>', type=int, help='School'
                          ' semester. For example, 201610 is Fall 2015 (take'
                          ' careful note that it uses the wrong year for fall'
                          ' terms), and 201620 is Spring 2016.')
    readline.add_argument('crn', metavar='<CRN>', type=int, help='Course'
                          ' request number.')

    args = readline.parse_args()
    course = PuCourse(args.term, args.crn)
    course.scrape()
    course.parse()

    if course.seats > 0 and course.waits <= 0:
        result = 'There are %s open seats in %s!' % (course.seats, course.name)
        print(result)

        if args.push:
            try:
                rc = push.config()
            except KeyError:
                push.fatal_unconfigured()

            push.push(rc, 'Purdue course watcher\n' + result)

if __name__ == '__main__':
    main()
