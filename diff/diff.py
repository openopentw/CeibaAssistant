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
def extract_table_horizon(soup): #return dictionary
    
    data = {}
    table = soup.find('table')

    rows = table.find_all('tr')
    for row in rows:
        index = row.find('th')
        index = re.sub("\r|\n","",index.text) 
        content = row.find('td')
        content = re.sub("\r|\n| ","",content.text)
        
        data[index] = content;
    for k,v in data.items():
        print ''.join(k).encode('utf8') + ' ' + ''.join(v).encode('utf8')
    
    return data
##################
def extract_table_vertical(soup): #return list
    data = []
    table = soup.find('table')

    rows = table.find_all('tr')
    index = []
    for row in rows:
        titles = row.find_all('th')
        if (len(titles) > 0) :
            
            for title in titles:
                title = re.sub("\r|\n| ","",title.text)
                index.append(title)
            continue 
        item = {}
        contents = []
        cols = row.find_all('td')
        for content in cols:
            content = re.sub("\r|\n| ","",content.text)
            contents.append(content)
        for i in range(len(index)):
            item[index[i]] = contents[i]

        data.append(item)

    for i in range(len(data)):
        for k,v in data[i].items():
            print ''.join(k).encode('utf8') + ' ' + ''.join(v).encode('utf8')
'''
    for i in range(len(data)):
        print ''.join(data[i][u'名稱']).encode('utf8')
'''

file = open('info.html','r')
#find h1 for html type
html = file.read()
soup = BeautifulSoup(html,'html.parser')
html_type = ''.join(soup.find('h1')).encode('utf8')
'''
print html_type
data = extract_table_vertical(soup)

'''
data = extract_table_horizon(soup)

##################
'''
#def diff(new,old):
for i in range(0,len(new)):
    new_class = new[i]
    old_class = old[i]
'''
#a = json.dumps(lecture[0])
