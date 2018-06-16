import os
from subprocess import call

# download = [
#     {
#         ChineseName: aaa,
#         EnglishName: bbb, #         Tutor: ccc,
#         Content: {
#             公佈欄:{
#                 名稱:link
#                 ...
#             }
#             課程內容:{
#                 周次:link
#                 ...
#             }
#             作業: {
#                 名稱:link
#                 ...
#             }		
#         }
#     },
# ]

# data/
#     aaa_bbb/
#         公布欄/
#             名稱_檔名
#         課程名稱/
#             周次_檔名
#         作業/
#             作業_檔名

test_item = [
        {
            'ChineseName': '數學之美',
            'EnglishName': 'Beauty of Math',
            'Tutor': '呂學一',
            'Content': {
                '公布欄': {},
                '課程內容': {
                    'bm2017spring-midterm2.pdf': 'https://ceiba.ntu.edu.tw/course/813cdf/content/bm2017spring-midterm2.pdf',
                    'bm2018spring01.pptx': 'https://ceiba.ntu.edu.tw/course/813cdf/content/bm2018spring01.pptx',
                    'bm2018spring05.pptx': 'https://ceiba.ntu.edu.tw/course/813cdf/content/bm2018spring05.pptx'
                },
                '作業': {}
            }
        },
        {
            'ChineseName': '密碼學導論',
            'EnglishName': 'Introduction to Cryptography',
            'Tutor': '陳君明',
            'Content': {
                '公布欄': {
                    '324762_2017 Exam 2.pdf': 'https://ceiba.ntu.edu.tw/course/725b8b/bulletin/324762_2017%20Exam%202.pdf',
                    '319922_2017 Exam 1.pdf': 'https://ceiba.ntu.edu.tw/course/725b8b/bulletin/319922_2017%20Exam%201.pdf',
                },
                '課程內容': {
                    '第1週-Syllabus 2017.pdf': 'https://ceiba.ntu.edu.tw/course/725b8b/content/Syllabus%202017.pdf',
                    '第4週-RC4_LFSR_Trivium.ppt': 'https://ceiba.ntu.edu.tw/course/725b8b/content/RC4_LFSR_Trivium.ppt',
                },
                '作業': {
                    'Quiz 1-檔案': 'https://ceiba.ntu.edu.tw/course/725b8b/hw/Quiz%201.pdf',
                    'Homework 1-檔案': 'https://ceiba.ntu.edu.tw/course/725b8b/hw/Crypto_hw1_2017.pdf',
                }
            }
        },
    ]

def check_dir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

def check_file(filename, link):
    if not os.path.isfile(filename):
        print('[CURL] %s\n[PATH] %s' % (link, filename))
        ret = call(["curl", link, '-o', filename])
        print('[STATUS] %s\n' % ('SUCCESS' if ret == 0 else 'FAIL'))

def get_link(link):
    if link.find('http') == -1:
        if link.find('course') == -1:
            return ''
        else:
            link = 'https://ceiba.ntu.edu.tw/' + link[link.find('course'):]
    return link

def trim_name(name):
    name = name.replace('/', '')
    name = name.replace('?', '')
    name = name.replace(' ', '_')
    name = name.replace('-', '')
    return name

def downloadfile(course_list, data_dir='data/'):
    print('[DOWNLOAD] Start to download files.')
    for c in course_list:
        course_dir = data_dir + trim_name(c['ChineseName']) + '_' + trim_name(c['EnglishName'])
        check_dir(course_dir)
        for c_type, content in c['Content'].items():
            content_dir = course_dir + '/' + c_type
            check_dir(content_dir)
            for f, link in content.items():
                f = trim_name(f)
                if link.split('.')[-1] != f.split('.')[-1] and link.find('.') != -1:
                    f +=  '.' + link.split('.')[-1]
                file_destination = content_dir + '/' + f
                link = get_link(link)
                if link != '':
                    check_file(file_destination, link)

if __name__ == '__main__':
    downloadfile(test_item)
