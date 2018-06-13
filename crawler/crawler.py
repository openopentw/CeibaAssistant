# -*- coding: utf-8 -*-
"""Download all html files from Ceiba.

This module download all html files from one's account, and organize them to a
dictionary.

"""

import json

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

class Crawler():
    """Download all html files from Ceiba with given cookie.

    Attributes:
        cookie: A cookie string that Ceiba gives you.
    """

    def __init__(self, cookie):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Cookie': cookie
        }

    def crawl(self, debug=False):
        """Download all html files from Ceiba with given cookie.

        Args:
            debug: A boolean indicating if the function output the debug json
                file or not.

        Returns:
            A list of dicts. In each dict, the keys are the attributes of that course.
            The keys are as follows:

                - ChineseName: string
                - EnglishName: string
                - Tutor: string
                - Content: dict

            And the keys in the dict `content` are as follows:

                - 課程資訊: html_sring
                - 教師資訊: html_sring
                - 公佈欄: {
                        - html:html_sring
                        - content: {
                            - 名稱:html_string
                            ...
                        }
                    }
                - 課程內容: html_sring
                - 作業區: {
                        - html: html_string
                        - content: {
                            - 名稱: html_string,
                            ...
                        }
                    }
                - 投票區: html_sring
                - 學習成績: html_sring

        """
        courses = self.get_courses()
        for course in courses:
            content = self.get_1st_htmls(course['url'])
            if content:
                # 公佈欄
                if content['公佈欄']:
                    bulletin = self.get_bulletin_htmls(content['公佈欄'])
                    content['公佈欄'] = {
                        'html': content['公佈欄'],
                        'content': bulletin,
                    }
                else:
                    content['公佈欄'] = {
                        'html': content['公佈欄'],
                        'content': {},
                    }

                # 作業區
                if content['作業區']:
                    bulletin = self.get_hw_htmls(content['作業區'])
                    content['作業區'] = {
                        'html': content['作業區'],
                        'content': bulletin,
                    }
                else:
                    content['作業區'] = {
                        'html': content['作業區'],
                        'content': {},
                    }

            course['content'] = content
        if debug:
            with open('./courses.json', 'w') as outfile:
                json.dump(courses, outfile)
        return courses

    def get_html_with_cookie(self, url, debug=False):
        req = Request(url, headers=self.headers)
        res = urlopen(req)
        html = res.read()
        if debug:
            with open('./tmp.html', 'w', encoding='utf8') as outfile:
                print(html)
                print(html.decode(), file=outfile)
        return html

    def get_courses(self, debug=False):
        url = 'https://ceiba.ntu.edu.tw/student/index.php'
        soup = BeautifulSoup(self.get_html_with_cookie(url), 'lxml')
        table = soup.find('table')
        rows = table.find_all('tr')[1:]

        courses = []
        for row in rows:
            tds = row.find_all('td')
            td4 = tds[4]

            td4_a = td4.find('a')
            chinese_name = td4_a.text.strip()
            url = td4_a['href']

            td4_a.extract()
            english_name = td4.text.strip()

            td5 = tds[5]
            td5_a = td5.find('a')
            tutor = td5_a.text.strip()

            courses += [{
                'ChineseName': chinese_name,
                'EnglishName': english_name,
                'Tutor': tutor,
                'url': url,
            }]

        if debug:
            with open('./tmp.json', 'w') as outfile:
                json.dump(courses, outfile)

        return courses

    def get_1st_htmls(self, url, debug=False):
        html = self.get_html_with_cookie(url)

        if b'frameset' not in html:
            return {}

        soup = BeautifulSoup(html, 'lxml')
        csn_url = soup.find('frameset').find_all('frame')[1]['src']
        csn = csn_url[csn_url.find('csn') + 4:]

        funs = {
            '課程資訊': 'info',
            '教師資訊': 'personal',
            '公佈欄': 'bulletin',
            '課程內容': 'syllabus',
            '投票區': 'vote',
            '討論看板': 'board',
            '作業區': 'hw',
            '學習成績': 'grade',
        }

        content = {}
        for idx in funs:
            if debug:
                print(idx)
            url = 'https://ceiba.ntu.edu.tw/modules/main.php?csn={}&default_fun={}&current_lang=chinese'.format(csn, funs[idx])
            if debug:
                print(url)
            html = self.get_html_with_cookie(url)
            if len(html) < 32:
                content[idx] = ''
            else:
                content[idx] = html.decode()

        if debug:
            with open('./tmp.json', 'w') as outfile:
                json.dump(content, outfile)

        return content

    def get_bulletin_htmls(self, html, debug=False):
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table')
        a_list = table.find_all('a')

        base_url = 'https://ceiba.ntu.edu.tw/modules/bulletin/'
        content = {}
        for a in a_list:
            url = base_url + a['href']
            html = self.get_html_with_cookie(url)
            content[a.text.strip()] = html.decode()

        if debug:
            with open('./tmp.json', 'w') as outfile:
                json.dump(content, outfile)

        return content

    def get_hw_htmls(self, html, debug=False):
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table')
        a_list = table.find_all('a')

        base_url = 'https://ceiba.ntu.edu.tw/modules/hw/'
        content = {}
        for a in a_list:
            url = base_url + a['href']
            html = self.get_html_with_cookie(url)
            content[a.text.strip()] = html.decode()

        if debug:
            with open('./tmp.json', 'w') as outfile:
                json.dump(content, outfile)

        return content

def main():
    cookie = 'Add your cookie here !'
    crawler = Crawler(cookie)
    courses = crawler.crawl(debug=True)

if __name__ == '__main__':
    main()
