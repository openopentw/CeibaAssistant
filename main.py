import os
import sys
from diff import diff
from helper_func import loginceiba
from helper_func.notify import Notifier
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
    # print(type(courses))
    notifications, calendars, downloads = diff.diff(courses[0], [])
    notifier = Notifier()
    notifier.show_diff_notifications(notifications)

    # for d in downlaods:
    #     diff.print_(d)
    downloadfile.downloadfile(downloads)
