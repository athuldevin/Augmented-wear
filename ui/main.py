import cv2
import cam
from calc import CalculatorWidget,Button
import pyautogui
from gallery import Pictures,Picture
import numpy as np
from copy import copy
from kivy.app import App
from kivy.clock import Clock
from functools import partial
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition
from kivy.properties import NumericProperty, ListProperty, ObjectProperty, DictProperty


camera=cam.cam(0)
Window.fullscreen = 'auto'
'''Window.borderless=1
Window.left=100
Window.top=100

Window.hieght=200
'''
KV = '''
#:import pi math.pi
#:import cos math.cos
#:import sin math.sin
#:import V kivy.vector.Vector
<ModernMenu>:
    canvas.before:
        Color:
            rgba: 0, 0, .9, .2
        Ellipse:
            pos: self.center_x - self.radius, self.center_y - self.radius
            size: self.radius * 2, self.radius * 2
            angle_start: 0
            angle_end: self.circle_progress * 360 * self.creation_direction
        Color:
            rgba: self.color
        Line:
            circle:
                (
                self.center_x, self.center_y,
                self.radius, 0, self.circle_progress * 360 * self.creation_direction
                )
            width: self.line_width
    on_touch_down:
        V(args[1].pos).distance(self.center) < self.radius and (
        self.back() if self.choices_history else self.dismiss())
<ModernMenuLabel>:
    size: self.texture_size
    padding: 5, 5
    on_press: self.callback and self.callback(self)
    canvas.before:
        Color:
            rgba: .31, .573, .816, .9
        Rectangle:
            pos: self.pos
            size: self.size
        Line:
            points:
                (
                self.center_x, self.center_y,
                self.parent.center_x + cos(
                self.opacity * self.index * 2 * pi / self.siblings
                ) * self.parent.radius,
                self.parent.center_y + sin(
                self.opacity * self.index * 2 * pi / self.siblings
                ) * self.parent.radius
                ) if self.parent else []
            width: self.parent.line_width if self.parent else 1
    center:
        (
        self.parent.center_x +
        cos(self.opacity * self.index * 2 * pi / self.siblings) * self.radius,
        self.parent.center_y +
        sin(self.opacity * self.index * 2 * pi / self.siblings) * self.radius
        ) if (self.size and self.parent and self.parent.children) else (0, 0)
'''


def dist(x,y):
    (x1, y1),(x2,y2)=x,y

    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


class ModernMenuLabel(ButtonBehavior, Label):
    index = NumericProperty(0)
    radius = NumericProperty(100)
    siblings = NumericProperty(1)
    callback = ObjectProperty(None)
    
    def on_parent(self, *args):
        if self.parent:
            self.parent.bind(children=self.update_siblings)

    def update_siblings(self, *args):
        if self.parent:
            self.siblings = max(0, len(self.parent.children))
        else:
            self.siblings = 1


class ModernMenu(Widget):
    radius = NumericProperty(50)
    circle_width = NumericProperty(5)
    line_width = NumericProperty(2)
    color = ListProperty([.31, .573, .816, .9])
    circle_progress = NumericProperty(0)
    creation_direction = NumericProperty(1)
    creation_timeout = NumericProperty(1)
    choices = ListProperty([])
    item_cls = ObjectProperty(ModernMenuLabel)
    item_args = DictProperty({'opacity': 0})
    animation = ObjectProperty(Animation(opacity=1, d=.5))
    choices_history = ListProperty([])

    def start_display(self, touch):
        touch.grab(self)
        a = Animation(circle_progress=1, d=self.creation_timeout)
        a.bind(on_complete=self.open_menu)
        touch.ud['animation'] = a
        a.start(self)

    def open_menu(self, *args):
        self.clear_widgets()
        for i in self.choices:
            kwargs = copy(self.item_args)
            kwargs.update(i)
            ml = self.item_cls(**kwargs)
            self.animation.start(ml)
            self.add_widget(ml)

    def open_submenu(self, choices, *args):
        self.choices_history.append(self.choices)
        self.choices = choices
        self.open_menu()


    def back(self, *args):
        self.choices = self.choices_history.pop()
        self.open_menu()

    def on_touch_move(self, touch, *args):
        if (
            touch.grab_current == self and
            dist(touch.pos, touch.opos) > self.radius and
            self.parent and
            self.circle_progress < 1
        ):
            self.parent.remove_widget(self)

        return True

    def on_touch_up(self, touch, *args):
        if (
            touch.grab_current == self and
            self.parent and
            self.circle_progress < 1
        ):
            self.parent.remove_widget(self)
        return True

    def dismiss(self):
        a = Animation(opacity=0)
        a.bind(on_complete=self._remove)
        a.start(self)

    def _remove(self, *args):
        if self.parent:
            self.parent.remove_widget(self)


class MenuSpawner(Widget):
    timeout = NumericProperty(0)
    menu_cls = ObjectProperty(ModernMenu)
    cancel_distance = NumericProperty(10)
    menu_args = DictProperty({})

    def on_touch_down(self, touch, *args):
        t = partial(self.display_menu, touch)
        touch.ud['menu_timeout'] = t
        Clock.schedule_once(t, self.timeout)
        return super(MenuSpawner, self).on_touch_down(touch, *args)

    def on_touch_move(self, touch, *args):
        if (
            touch.ud['menu_timeout'] and
            dist(touch.pos, touch.opos) > self.cancel_distance
        ):
            Clock.unschedule(touch.ud['menu_timeout'])
        return super(MenuSpawner, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch, *args):
        if touch.ud.get('menu_timeout'):
            Clock.unschedule(touch.ud['menu_timeout'])
        return super(MenuSpawner, self).on_touch_up(touch, *args)

    def display_menu(self, touch, dt):
        menu = self.menu_cls(center=touch.pos, **self.menu_args)
        self.add_widget(menu)
        menu.start_display(touch)


class Home(Screen):
    Builder.load_file("kv/home.kv")
    
Builder.load_string(KV)
Builder.load_file("kv/calculator.kv")
Builder.load_file("kv/gallery.kv")
class ModernMenuApp(App):
    def build(self):
        self.sm=ScreenManager(transition=FadeTransition())
        self.sm.add_widget(Home(name='home'))
        self.sm.add_widget(CalculatorWidget(name='calculator'))
        self.sm.add_widget(Pictures(name='pictures'))
        cam.cam_num=0
        Clock.schedule_interval(camera.frame,(1/10))
        
        return self.sm

    def calculator(self, *args):
        args[0].parent.dismiss()
        self.sm.current="calculator"

    def pictures(self, *args):
        args[0].parent.dismiss()
        self.sm.current="pictures"

    def callback1(self, *args):
        print ("test 1")
        args[0].parent.open_submenu(
            choices=[
                dict(text='action 1', index=1, callback=self.callback2),
                dict(text='action 2', index=2, callback=self.callback2),
                dict(text='action 3', index=3, callback=self.callback2),
            ])

    def callback2(self, *args):
        print ("test 2")
        args[0].parent.dismiss()

    def callback3(self, *args):
        print ("test 3")
        args[0].parent.dismiss()

    def callback4(self, *args):
        print ("test 4")
        args[0].parent.open_submenu(
            choices=[
                dict(text='hai', index=1, callback=self.callback2),
                dict(text='oh', index=2, callback=self.callback2),
            ])

    def callback5(self, *args):
        print ("exit")
        App.get_running_app().stop()
        args[0].parent.dismiss()


if __name__ == '__main__':
    ModernMenuApp().run()
