from gi.repository import Notify


class Notifier():
    def __init__(self):
        Notify.init('Ceiba Assistant')

    def _show_notification(self, **kwargs):
        message = Notify.Notification.new(**kwargs)
        message.show()


if __name__ == '__main__':
    notify = Notifier()
    content = {
        'summary': '新的課程簡報',
        'body': '這堂課程在 Ceiba 上傳了新的簡報',
        'icon': 'document-open',
    }
    notify._show_notification(**content)
