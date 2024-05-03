from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.home_screen import HomeScreen
from screens.top_screen import TopScreen
from screens.article_list_screen import ArticleListScreen
from screens.article_screen import ArticleScreen

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(TopScreen(name='top'))
        sm.add_widget(ArticleListScreen(name='articles'))
        sm.add_widget(ArticleScreen(name='article'))
        return sm

if __name__ == '__main__':
    MyApp().run()
