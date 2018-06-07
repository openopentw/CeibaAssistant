 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import json
lecture =  [
    {
        'ChineseName' : 'aaa',
        'EnglishName' : 'bbb',
        'Tutor' : 'ccc',
        'Content': {
            '課程資訊': 'html_sring',
            '教師資訊': 'html_sring',
            '公佈欄': 'html_sring',
            '課程內容': 'html_sring',
            '作業區': {
                'html': 'html_string',
                'content': [
                    'html_string'
                ]
            },
            '投票區': 'html_sring',
            # TODO: 討論看版: html_sring
            '學習成績': 'html_sring'
        }
    }
]

#extract table without link
'''
課程資訊&教師資訊 表格結構一樣
剩下也一樣
'''
def extract_table_horizon(soup):
    
    data = {}
    table = soup.find('table')

    rows = table.find_all('tr')
    for row in rows:
        index = row.find('th')
        index = re.sub("\r|\n","",index.text) 
        content = row.find('td')
        content = re.sub("\r|\n","",content.text)
        
        data[index] = content;

    print ''.join(data[u'課號']).encode('utf8')
    
    return data
##################

file = open('info.html','r')
#find h1 for html type
html = file.read()
soup = BeautifulSoup(html,'html.parser')
html_type = ''.join(soup.find('h1')).encode('utf8')
if html_type == '課程資訊':
    print u'是 課程資訊啦...'
    data = extract_table_horizon(soup)
else:
    print html_type
    print '88888'
##################
'''
#def diff(new,old):
for i in range(0,len(new)):
    new_class = new[i]
    old_class = old[i]
'''
#a = json.dumps(lecture[0])
