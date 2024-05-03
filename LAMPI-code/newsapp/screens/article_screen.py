from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from .objects.line_separator import LineSeparator
import paho.mqtt.publish as publish
import pandas as pd
import json


class ArticleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True, scroll_type=['bars', 'content'])

        self.back_btn = Button(text=' <-- ', size_hint_y=None, height=50)
        self.back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_btn)

        self.title_label = Label(color=(1, 1, 1, 1), size_hint_y=None, halign='left', valign='middle')
        self.title_label.bind(size=self.update_text_size)
        self.layout.add_widget(self.title_label)
        self.layout.add_widget(LineSeparator())

        self.item_type_label = Label(color=(1, 1, 1, 1), size_hint_y=None, halign='left', valign='middle')
        self.item_type_label.bind(size=self.update_text_size)
        self.layout.add_widget(self.item_type_label)
        self.layout.add_widget(LineSeparator())

        self.abstract_label = Label(color=(1, 1, 1, 1), size_hint_y=None, halign='left', valign='middle')
        self.abstract_label.bind(size=self.update_text_size)
        self.layout.add_widget(self.abstract_label)
        self.layout.add_widget(LineSeparator())

        self.add_to_list_btn = Button(text='Add to Reading List', size_hint_y=None, height=50)
        self.add_to_list_btn.bind(on_press=self.handle_add_to_list)
        self.layout.add_widget(self.add_to_list_btn)

        scroll_view.add_widget(self.layout)
        self.add_widget(scroll_view)

        self.url = None
        self.title = None

    def update_text_size(self, instance, value):
        padding = 20
        instance.text_size = (instance.width - padding, None)

    def display_article(self, title, url, abstract, item_type):
        self.title_label.text = f"Title: {title}"
        self.item_type_label.text = f"Type: {item_type}"
        self.abstract_label.text = f"Abstract: {abstract}"
        self.url = url
        self.title = title

    def handle_add_to_list(self, instance):
        if self.title and self.url:
            self.add_to_reading_list(self.title, self.url)

    def go_back(self, instance):
        self.manager.current = self.manager.previous()

    def add_to_reading_list(self, title, url):
        msg = {'title': title, 'url': url}
        msg = json.dumps(msg).encode('utf-8')
        publish.single("devices/b827eb309ede/news/", msg, hostname="34.207.111.28", port=50001)
