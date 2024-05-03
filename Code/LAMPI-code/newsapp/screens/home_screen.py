from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        top_btn = Button(text='Top')
        top_btn.bind(on_press=self.go_to_top)
        recent_btn = Button(text='Recent')
        recent_btn.bind(on_press=self.go_to_recent)
        layout.add_widget(top_btn)
        layout.add_widget(recent_btn)
        self.add_widget(layout)

    def go_to_top(self, instance):
        self.manager.current = 'top'

    def go_to_recent(self, instance):
        self.manager.current = 'articles'
        self.manager.get_screen('articles').list_articles(None)
