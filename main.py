#!/usr/bin/env python3
import os
import getpass
import argparse
import configparser

from diff import diff
from helper_func import loginceiba
from helper_func.notify import Notifier
import downloadfile
from crawler.crawler import Crawler


def default_config_filepath(create=False):
    if 'XDG_CONFIG_HOME' in os.environ:
        # follow XDG base directory specification
        config_path = os.path.join(os.environ['XDG_CONFIG_HOME'], 'ceiba-assistant', 'config.ini')
        if os.path.isfile(config_path) or create:
            return config_path
    elif 'HOME' in os.environ:
        config_path = os.path.join(os.environ['HOME'], '.ceiba-assistant', 'config.ini')
        if os.path.isfile(config_path) or create:
            return config_path
    else:
        config_path = 'config.ini'
        if os.path.isfile(config_path) or create:
            return config_path

    # Cannot find an existed config file. Create one.
    config_path = default_config_filepath(create=True)
    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    config_template = """
        [account]
        student  = {}
        password = {}
        semester = {}
    """
    with open(config_path, 'w') as config:
        config.write(config_template.format(input('輸入學號: '),
                                            getpass.getpass('輸入密碼: '),
                                            input('輸入學期: ')))
    return config_path


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
    parser.add_argument('-c', '--config', action='store',
                        help='path to configuration file')
    options = parser.parse_args()
    options.config = options.config or default_config_filepath()

    config = configparser.ConfigParser()
    config.read(options.config)

    main(config)
