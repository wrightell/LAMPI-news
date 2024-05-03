from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

class LineSeparator(GridLayout):
    def __init__(self, **kwargs):
        super(LineSeparator, self).__init__(size_hint_y=None, height=1, cols=1, **kwargs)
        with self.canvas.before:
            Color(0.7, 0.7, 0.7, 1)  # grey color
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
