#!/usr/bin/env python3
import argparse
import configparser
from bs4 import BeautifulSoup
import requests

import main
import parse
from helper_func import loginceiba
from crawler.crawler import Crawler


def submit_homework_form(crawler, url, file):
    html = crawler.get_html_with_cookie(url)
    args = {
        'cookies': dict(item.split('=') for item in crawler.headers['Cookie'].split('; ')),
        'data': parse.parse_form(html),
        'files': {'file': open(file, 'rb')},
    }
    return requests.post(url, **args)


def check_submit_response(response):
    return BeautifulSoup(response.content.decode(), 'html5lib').select_one('body')['onload'] == "Page_load('hw_upload','1')"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ceiba Assistant')
    parser.add_argument('-c', '--config', action='store',
                        help='path to configuration file')
    options = parser.parse_args()
    options.config = options.config or main.default_config_filepath()

    config = configparser.ConfigParser()
    config.read(options.config)

    login_args = '{student} {password} {semester}'.format(**config['account'])
    cookie = loginceiba.info(*login_args.split())
    crawler = Crawler(cookie)

    # If ignored: 使用錯誤
    url = 'https://ceiba.ntu.edu.tw/1062VC'
    crawler.get_html_with_cookie(url)
    # If ignored: 您非修課學生
    url = 'https://ceiba.ntu.edu.tw/modules/hw/hw.php'
    crawler.get_html_with_cookie(url)

    response = submit_homework_form(crawler, 'https://ceiba.ntu.edu.tw/modules/hw/hw_show.php?current_lang=chinese&hw_sn=201428', '/home/redbug312/empty')
    print(response.content.decode())
