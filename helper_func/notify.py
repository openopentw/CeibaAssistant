#!/usr/bin/env python3


class Notifier():
    def __init__(self, gui='gtk'):
        gui_notifier = {
            'gtk': GtkNotifier,
            'qt': QtNotifier,
        }
        self.notifier = gui_notifier[gui]()
        self.templates = {
            '公佈欄': self.create_message_template('{}課程張貼了公佈'),
            '作業區': self.create_message_template('{}課程張貼了作業'),
            '投票區': self.create_message_template('{}課程張貼了投票'),
            '學習成績': self.create_message_template('{}課程張貼了成績'),
        }

    def create_message_template(self, summary, body='{:1}', icon='document-open'):
        def template(key, diff):
            formatted_summary = summary.format(diff['ChineseName'])
            formatted_bodies = [body.format(*pair) for pair in diff['Content'][key].items()]
            if len(formatted_bodies) > 3:
                formatted_bodies = formatted_bodies[:2] + ['...']
            return (formatted_summary, '\n'.join(formatted_bodies), icon)
        return template

    def collect_message_from_diff(self, course_diff):
        message = [self.templates[key](key, course_diff) for key in self.templates.keys()
                   if key in course_diff['Content'] and course_diff['Content'][key]]
        return message

    def show_diff_notifications(self, course_diffs):
        for messages in map(self.collect_message_from_diff, course_diffs):
            for message in messages:
                self._show_notification(*message)

    def _show_notification(self, summary, body, icon='document-open'):
        self.notifier._show_notification(summary, body, icon)


class GtkNotifier:
    def __init__(self):
        from gi.repository import Notify
        Notify.init('Ceiba Assistant')

    def _show_notification(self, *args):
        from gi.repository import Notify
        message = Notify.Notification.new(*args)
        message.show()


class QtNotifier:
    def __init__(self):
        import sys
        from PyQt5 import Qt
        self.dummy = Qt.QApplication(sys.argv)

    def _show_notification(self, *args):
        from PyQt5 import Qt
        icon = Qt.QIcon.fromTheme(args[2])
        tray = Qt.QSystemTrayIcon(icon, self.dummy)
        tray.show()
        tray.showMessage(*args[:2], icon)


if __name__ == '__main__':
    notify = Notifier()
    content = [
        '新的課程簡報',
        '這堂課程在 Ceiba 上傳了新的簡報',
    ]
    diff = [{'ChineseName': 'aaa', 'EnglishName': 'bbb', 'Tutor': 'ccc', 'Content': {'課程資訊': {}, '上課時間': '星期一6,7', '上課地點': '博雅103', '公佈欄': {'期中考說明書': '大家好，附件為本次期中考的說明書，相信平常就在磨練技藝的你們，照此說明書上寫的攻略指南，一定能順利面對邏輯期中考這個小怪！請大家務必抽空看一下。座位表最遲本周五晚間公布，考試時請依座位表入座，並攜帶學生證備查。下周就要期中考了，大家準備考試時，如有任何問題，歡迎來信詢問助教。二位助教都可以問，雖然洵渼人在德國，但他還是會克服時差干擾替大家解惑哦∼複習一下助教的信箱：陳洵渼：r98124017@gmail.com；許小花：bookitchen@gmail.com原則上第一組找阿渼，第二組找小花；寄了很久要是沒人回，就兩位都寄吧！助教們下周一中午會提早到教室，大家也可利用最後的緊要關頭發問。最後，祝大家讀到的都有考、考到的都有讀到∼小花'}, '課程內容': {}, '作業區': {}, '投票區': {}, '學習成績': {'期中考': '81', '期末考': '555', '加分小卡': '--', '作業一': 'A+', '作業二': 'A', '作業三': 'X', '作業四': 'A+', '作業五': 'A+', '學期成績': '--'}}}]
    notify.show_diff_notifications(diff)
