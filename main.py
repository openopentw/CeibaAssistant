import os
import sys
#from helper_func import loginceiba
sys.path.append('helper_func') #temp
import loginceiba #temp
import diff
import notify
import downloadfile
from crawler import Crawler

cookie = loginceiba.info('b07902000', '*****', '1062')
if cookie == 1:
    print("can't login!!")
else:
    print('login_success, cookie:')
    print(cookie)
    crawler = Crawler(cookie.strip('\n'))
    courses = crawler.crawl()
    #print(type(courses))
    notifications,calendars ,downlaods = diff.diff(courses[0],[])

    #diff.print_(downlaods[0])
    downloadfile.downloadfile(downlaods)
