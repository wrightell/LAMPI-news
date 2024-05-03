from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.metrics import dp


class TopScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        sections = [
            'arts', 'automobiles', 'business', 'fashion', 'food',
            'health', 'insider', 'magazine', 'movies', 'nyregion', 'obituaries',
            'opinion', 'politics', 'realestate', 'science', 'sports', 'sundayreview',
            'technology', 'theater', 't-magazine', 'travel', 'upshot', 'us', 'world'
        ]

        back_btn = Button(text=' <-- ', size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        home_btn = Button(text='FRONT PAGE',size_hint_y=None,height=dp(48))
        home_btn.bind(on_press=lambda instance :self.view_section(Button(text='home')))
        layout.add_widget(home_btn)

        for section in sections:
            btn = Button(text=section, size_hint_y=None, height=dp(48))
            btn.bind(on_press=self.view_section)
            layout.add_widget(btn)

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(layout)

        self.add_widget(scroll_view)

    def view_section(self, instance):
        self.manager.current = 'articles'
        self.manager.get_screen('articles').list_articles(instance.text)

    def go_back(self, instance):
        self.manager.current = self.manager.previous()