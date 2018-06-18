#!/usr/bin/env python3
import json
import webbrowser

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import cli


class UploadPage:
    def __init__(self, label, page):
        self.label = Gtk.Label(label)
        self.content = Gtk.ListBox()
        for item in page:
            row = Gtk.ListBoxRow()
            row.add(Gtk.Label(item[0]))
            row._link = item[1]
            self.content.add(row)
        self.content.show_all()


class Uploader:
    def __init__(self, cookie=None):
        Gtk.init()
        self.cookie = cookie
        self.builder = self.build_ui()
        self.selected_link = None

    def start(self):
        Gtk.main()

    def cleanup(self):
        pass

    def build_ui(self):
        builder = Gtk.Builder()
        builder.add_from_file('uploader.glade')
        builder.connect_signals(self)
        builder.get_object('window').show()
        return builder

    # Coustomized methods
    def add_page(self, page):
        self.builder.get_object('notebook').append_page(page.content, page.label)
        page.content.connect('row-selected', self.on_row_selected)

    # Receive signals
    def on_window_delete_event(self, widget, event=None):
        Gtk.main_quit()

    def on_row_selected(self, widget, event=None):
        self.selected_link = widget.get_selected_row()._link

    def on_cancel_button_clicked(self, widget, event=None):
        self.on_window_delete_event(widget)

    def on_open_button_clicked(self, widget, event=None):
        """
        Noted that the link would be correctly opened only if
        1. Users just logined in Ceiba with their browser, and
        2. The button.php grimoire was used or the users clicked it themselves

        Since webbrowser don't take POST fields or headers as parameters, to
        open Ceiba website from browsers might be difficult
        """
        print('Try to open {}'.format(self.selected_link))
        if self.selected_link:
            webbrowser.open(self.selected_link)


def _main():
    uploader = Uploader()

    with open('courses.json', 'r') as courses_data:
        courses = json.load(courses_data)

    for course in map(cli.parse_course, courses):
        if course['作業區'] is None:
            continue
        name = course['課程資訊']['課程名稱']
        hws = [tuple(hw['名稱'].items())[0] for hw in course['作業區']]
        hws = [(hw[0], 'https://ceiba.ntu.edu.tw/modules/hw/' + hw[1])for hw in hws]
        uploader.add_page(UploadPage(name, hws))

    uploader.start()
    uploader.cleanup()


if __name__ == '__main__':
    _main()
