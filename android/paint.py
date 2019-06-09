from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line,Color, Rectangle, Point, GraphicException
from kivy.uix.button import Button 
from random import random
from math import sqrt
from kivy.uix.widget import Widget
import sys,os
import pickle

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
    
class Painter(Screen, FloatLayout, Widget):
    def __init__(self,**kwargs):
        super(Painter,self).__init__(**kwargs)
        self.group=[]
        self.point_data = []

    def show (self, file_name):
        print ("inside show")
        self.fname = file_name
    def on_pause(self):
        return True

    def back (self):
        self.manager.current = "home"

    def on_touch_down(self, touch):
        ud = touch.ud
        ud['group'] = g = str(touch.uid)
        with self.canvas:
            ud['color'] = Color(.31, .573, .816, mode='rgb', group=g)
            ud['lines'] = (
                
                Point(points=(touch.x, touch.y), source='particle.png',
                      pointsize=5, group=g))
            if (self.draw):
                for [x,y] in self.point_data :
                    ud['lines'] = (Point(points=(x,y), source='particle.png',pointsize=5, group=g))
                self.draw = False

        self.point_data.append([touch.x, touch.y])
        touch.grab(self)
        ret = super(Painter, self).on_touch_down(touch)
        return False

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return
        ud = touch.ud
        

        points = ud['lines'].points
        oldx, oldy = points[-2], points[-1]
        points = calculate_points(oldx, oldy, touch.x, touch.y)
        print (points)
        if points:
            try:
                lp = ud['lines'].add_point
                for idx in range(0, len(points), 2):
                    lp(points[idx], points[idx+1])
                    self.point_data.append([points[idx], points[idx+1]])
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
    
    def on_leave (self, **kwargs):
        curdir = os.path.dirname(__file__)
        cur=os.path.join(curdir, 'paint', self.fname)
        curdir=os.path.join(curdir, 'data', self.fname+'.dat')
        self.clear_widgets()
        self.export_to_png(cur)
        self.add_widget(self.ids.te)
        self.add_widget(self.ids.test)
        with open(curdir, 'wb+') as fp:
            pickle.dump(self.point_data, fp)

    def on_enter (self, **kwargs):
        curdir = os.path.dirname(__file__)
        curdir=os.path.join(curdir, 'data', self.fname+".dat")
        try:
            with open (curdir, 'rb+') as fp:
                self.point_data = pickle.load(fp)
                self.draw = True
        except Exception as identifier:
            self.draw = False
        