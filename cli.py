#!/usr/bin/env python3
import json
from bs4 import BeautifulSoup

from diff import diff


filter_newlines = str.maketrans('', '', '\r\n')
strip_text = lambda raw: raw.text.strip().translate(filter_newlines)
strip_texts = lambda raws: '\n'.join(map(strip_text, raws))


def parse_table(html, alternative=False):
    try:
        table = BeautifulSoup(html, 'html5lib').select_one('table')

        if table.find('thead'):  # it's a table
            if alternative:
                select_th = map(strip_text, table.select('thead th'))
                result = [{th: strip_text(td) for th, td in zip(select_th, tr.select('td'))}
                          for tr in table.select('tbody tr')[1:]]
            else:
                result = diff.extract_table_horizon(table.parent)
        else:  # it's a list in table
            if alternative:
                select_th = map(strip_text, table.select('tr th'))
                result = {th: strip_texts(tr.select('td')) for th, tr in zip(select_th, table.select('tr'))}
            else:
                result = diff.extract_table_vertical(table.parent)
    except AttributeError:
        return None
    else:
        return result


def parse_course(course):
    parse_fun = {
        '課程資訊': lambda json: parse_table(json, alternative=True),
        '教師資訊': parse_table,
        '公佈欄'  : lambda json: map(parse_table, json['Content'].values()),
        '課程內容': parse_table,
        '討論看板': lambda json: parse_table(json),
        '作業區'  : lambda json: parse_table(json['html']),
        '投票區'  : parse_table,
        '學習成績': parse_table,
    }
    return {key: parse_fun[key](value) for key, value in course['Content'].items()}


with open('courses.json', 'r') as courses_data:
    courses = json.load(courses_data)
    courses = map(parse_course, courses)
