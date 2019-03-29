from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.uix.button import Button 

class backButton(Button):
    pass

class Painter(Screen,Widget):
    def on_touch_down(self,touch):
        with self.canvas:
            touch.ud["line"] = Line(points=(touch.x,touch.y))

    def on_touch_move(self,touch):
        touch.ud["line"].points += [touch.x,touch.y]