from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from NYTConnector import NYTConnector


class ArticleListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.scroll_view.add_widget(self.layout)

        self.add_widget(self.scroll_view)
        self.back_btn = Button(text=' <-- ', size_hint_y=None, height=50)
        self.back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_btn)
        self.conn = NYTConnector()
        self.dyn_widgets = []

    def list_articles(self, section):
        for widget in self.dyn_widgets:
            self.layout.remove_widget(widget)
        self.dyn_widgets=[]

        if section is None:
            articles_df = self.conn.get_recent_stories()
        else:
            articles_df = self.conn.get_top_stories(section)
        if articles_df is None:
            btn = Button(text='No Articles')
            self.layout.add_widget(btn)
            self.dyn_widgets.append(btn)
            return
        for _, row in articles_df.iterrows():
            btn = Button(text=row['title'], size_hint_y=None, height=dp(48), halign='left')
            btn.shorten = True 
            btn.shorten_from = 'right' 
            btn.padding = (dp(0.1), 0) 
            btn.text_size = (btn.width, None) 
            btn.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)),on_press=lambda instance, title=row['title'], url=row['url'], abstract=row['abstract'], item_type=row['item_type']: self.view_article(instance, title, url, abstract, item_type))
            self.layout.add_widget(btn)
            self.dyn_widgets.append(btn)


    def view_article(self, instance, title, url, abstract, item_type):
        print(f"Title: {title}, URL: {url}, Abstract: {abstract}, Item Type: {item_type}")
        self.manager.current = 'article'
        self.manager.get_screen('article').display_article(title, url, abstract, item_type)

    def go_back(self, instance):
        self.manager.current = self.manager.previous()