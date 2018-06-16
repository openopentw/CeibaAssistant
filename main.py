import os
import sys
#from helper_func import loginceiba
sys.path.append('helper_func') #temp
import loginceiba #temp
from diff import diff
import notify
import downloadfile
from crawler.crawler import Crawler

cookie = loginceiba.info('b00000000', '****', '1062')
if cookie == 1:
    print("can't login!!")
else:
    print('login_success, cookie:')
    print(cookie)
    crawler = Crawler(cookie.strip('\n'))
    courses = crawler.crawl()
    #print(type(courses))
    notifications,calendars ,downlaods = diff.diff(courses[0],[])

    # for d in downlaods:
    #     diff.print_(d)
    downloadfile.downloadfile(downlaods)
