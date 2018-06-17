import argparse
import configparser

from diff import diff
from helper_func import loginceiba
from helper_func.notify import Notifier
import downloadfile
from crawler.crawler import Crawler


def main(config):
    login_args = '{student} {password} {semester}'.format(**config['account'])
    cookie = loginceiba.info(*login_args.split())

    if cookie == 1:
        print("can't login!!")
        return

    print('login_success, cookie:')
    print(cookie)

    crawler = Crawler(cookie.strip('\n'))
    courses = crawler.crawl()

    notifications, calendars, downloads = diff.diff(courses[0], [])
    notifier = Notifier()
    notifier.show_diff_notifications(notifications)
    downloadfile.downloadfile(downloads)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ceiba Assistant')
    parser.add_argument('-c', '--config', action='store', metavar='config')
    options = parser.parse_args()
    options.config = options.config or 'config.ini'

    config = configparser.ConfigParser()
    config.read(options.config)
    main(config)
