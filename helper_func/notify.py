#!/usr/bin/env python3


class Notifier():
    def __init__(self, gui='gtk'):
        gui_notifier = {
            'gtk': GtkNotifier,
            'qt': QtNotifier,
        }
        self.notifier = gui_notifier[gui]()

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
    notify = Notifier('qt')
    content = [
        '新的課程簡報',
        '這堂課程在 Ceiba 上傳了新的簡報',
    ]
    notify._show_notification(*content)
