#!/usr/bin/env python3
import os
import json
import argparse
import configparser

import cli
import main
import submit
from helper_func import loginceiba
from crawler.crawler import Crawler

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class UploadPage:
    def __init__(self, label, page):
        self.label = Gtk.Label(label)
        self.content = Gtk.ListBox()
        for item in page:
            row = Gtk.ListBoxRow()
            row.add(Gtk.Label(item[0]))
            row._links = item[1]
            self.content.add(row)
        self.content.show_all()


class Uploader:
    def __init__(self, crawler=None, file=''):
        Gtk.init()
        self.crawler = crawler
        self.file = file
        self.builder = self.build_ui()
        self.selected_links = None

    def start(self):
        Gtk.main()

    def cleanup(self):
        pass

    def build_ui(self):
        ui_glade = os.path.join(os.path.dirname(__file__), 'uploader-gtk.glade')
        builder = Gtk.Builder()
        builder.add_from_file(ui_glade)
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
        self.selected_links = widget.get_selected_row()._links

    def on_cancel_button_clicked(self, widget, event=None):
        self.on_window_delete_event(widget)

    def on_open_button_clicked(self, widget, event=None):
        print('Try to open {}'.format(self.selected_links[-1]))
        if self.selected_links is None:
            return
        for link in self.selected_links[:-1]:
            self.crawler.get_html_with_cookie(link)
        response = submit.submit_homework_form(self.crawler, self.selected_links[-1], self.file)
        print(submit.check_submit_response(response))


def _main(option, config):
    login_args = '{student} {password} {semester}'.format(**config['account'])
    cookie = loginceiba.info(*login_args.split())
    crawler = Crawler(cookie)
    uploader = Uploader(crawler, option.file)

    course_cache = os.path.join(os.path.dirname(__file__), 'courses.json')
    with open(course_cache, 'r') as courses_data:
        courses = json.load(courses_data)

    for course in map(cli.parse_course, courses):
        # from pprint import pprint
        # pprint(course)
        if course['作業區'] is None:
            continue
        get_links = lambda hw_url: [
            course['課程資訊']['課程網址'],
            'https://ceiba.ntu.edu.tw/modules/hw/hw.php',
            'https://ceiba.ntu.edu.tw/modules/hw/' + hw_url
        ]
        name = course['課程資訊']['課程名稱']
        hws = [tuple(hw['名稱'].items())[0] for hw in course['作業區']]
        hws = [(hw[0], get_links(hw[1])) for hw in hws]
        uploader.add_page(UploadPage(name, hws))

    uploader.start()
    uploader.cleanup()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ceiba Assistant')
    parser.add_argument('-f', '--file', action='store', required=True,
                        help='path to file for uploading')
    parser.add_argument('-c', '--config', action='store',
                        help='path to configuration file')
    options = parser.parse_args()
    options.config = options.config or main.default_config_filepath()

    config = configparser.ConfigParser()
    config.read(options.config)

    _main(options, config)
