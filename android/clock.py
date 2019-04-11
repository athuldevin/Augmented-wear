from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.floatlayout import FloatLayout
from math import cos, sin, pi
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ButtonBehavior 

import datetime

kv = '''
#:import math math

[ClockNumber@Label]:
    text: str(ctx.i)
    pos_hint: {"center_x": 0.5+0.42*math.sin(math.pi/6*(ctx.i-12)), "center_y": 0.5+0.42*math.cos(math.pi/6*(ctx.i-12))}
    font_size: self.height/8
<ClockNumber>:
	color: [.31, .573, .816, .9]

<MyClockWidget>:
    face: face
    ticks: ticks
    FloatLayout:
        id: face
        size_hint: None, None
        pos_hint: {"center_x":0.5, "center_y":0.5}
        size: 0.9*min(root.size), 0.9*min(root.size)
        canvas:
            Color:
                rgb: 0, 0, 0
            Ellipse:
                size: self.size     
                pos: self.pos
        ClockNumber:
            i: 1
        ClockNumber:
            i: 2
        ClockNumber:
            i: 3
        ClockNumber:
            i: 4
        ClockNumber:
            i: 5
        ClockNumber:
            i: 6
        ClockNumber:
            i: 7
        ClockNumber:
            i: 8
        ClockNumber:
            i: 9
        ClockNumber:
            i: 10
        ClockNumber:
            i: 11
        ClockNumber:
            i: 12
    Ticks:
        id: ticks
        r: min(root.size)*0.9/2
    
'''
Builder.load_string(kv)

class MyClockWidget(Screen,FloatLayout):
    pass
class Ticks(ButtonBehavior,Widget):
    def __init__(self, **kwargs):
        super(Ticks, self).__init__(**kwargs)
        self.bind(pos=self.update_clock)
        self.bind(size=self.update_clock)
        Clock.schedule_interval(self.update_clock, 1)
    
    def on_release(self):
        print('here')
        self.parent.manager.current='home'

    def update_clock(self, *args):
        self.canvas.clear()
        with self.canvas:
            time = datetime.datetime.now()
            Color(.31, .573, .816, .9)
            Line(points=[self.center_x, self.center_y, self.center_x+0.8*self.r*sin(pi/30*time.second), self.center_y+0.8*self.r*cos(pi/30*time.second)], width=2, cap="round")
            Color(.31, .573, .816, .9)
            Line(points=[self.center_x, self.center_y, self.center_x+0.7*self.r*sin(pi/30*time.minute), self.center_y+0.7*self.r*cos(pi/30*time.minute)], width=4, cap="round")
            Color(.31, .573, .816, .9)
            th = time.hour*60 + time.minute
            Line(points=[self.center_x, self.center_y, self.center_x+0.5*self.r*sin(pi/360*th), self.center_y+0.5*self.r*cos(pi/360*th)], width=6, cap="round")

class MyClockApp(App):
    def build(self):
        clock = MyClockWidget()
        Clock.schedule_interval(clock.ticks.update_clock, 1)
        return clock

if __name__ == '__main__':
    MyClockApp().run()
