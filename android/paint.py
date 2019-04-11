from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line,Color, Rectangle, Point, GraphicException
from kivy.uix.button import Button 
from random import random
from math import sqrt
from kivy.uix.widget import Widget

class backButton(Button):
    pass

def calculate_points(x1, y1, x2, y2, steps=5):
    dx = x2 - x1
    dy = y2 - y1
    dist = sqrt(dx * dx + dy * dy)
    if dist < steps:
        return None
    o = []
    m = dist / steps
    for i in range(1, int(m)):
        mi = i / m
        lastx = x1 + dx * mi
        lasty = y1 + dy * mi
        o.extend([lastx, lasty])
    return o

class Painter(Screen,FloatLayout):
    def __init__(self,**kwargs):
        super(Painter,self).__init__(**kwargs)
class Draw(Widget):
    def __init__(self, **kwargs):
        super(Draw,self).__init__(**kwargs)
        self.group=[]
    def on_touch_down(self, touch):
        ud = touch.ud
        ud['group'] = g = str(touch.uid)
        with self.canvas:
            ud['color'] = Color(1, 1, 1, mode='rgb', group=g)
            ud['lines'] = (
                
                Point(points=(touch.x, touch.y), source='particle.png',
                      pointsize=5, group=g))

        
        touch.grab(self)
        ret = super(Draw, self).on_touch_down(touch)
        return False

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return
        ud = touch.ud
        

        points = ud['lines'].points
        oldx, oldy = points[-2], points[-1]
        points = calculate_points(oldx, oldy, touch.x, touch.y)
        if points:
            try:
                lp = ud['lines'].add_point
                for idx in range(0, len(points), 2):
                    lp(points[idx], points[idx+1])
            except GraphicException:
                pass

        

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return
        touch.ungrab(self)
        self.ud = touch.ud
        self.group.append(self.ud['group']) 
        
    def undo(self):
        try:
            self.canvas.remove_group(self.group.pop())
            self.canvas.remove_group(self.group.pop())
        except :
            pass          
        
        
    