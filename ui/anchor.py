from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.app import App
from kivy.lang import Builder

from random import random

kv = '''
<ColoredLabel>:
    background_color:
    canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size
'''

Builder.load_string(kv)

class ColoredLabel(Label):
    background_color = ListProperty((0, 0, 0, 1))

class TestApp(App):
    def build(self):
        layout = BoxLayout(pos=(50,50), size=(10,5))
        for label in ('a', 'b', 'c', 'd'):
            label = ColoredLabel(text=label, background_color=(random(), random(), random(), 1))
            layout.add_widget(label)

        return layout

if __name__ == '__main__':
    TestApp().run()
