from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.behaviors.button import ButtonBehavior 
from kivy.uix.widget import Widget
import socket
import datetime
import random 
import sys,os
from kivy.lang import Builder
from kivy.properties import NumericProperty
class Calibrate(Screen, Widget):
    

    [a,b] = Window.size
    w = NumericProperty(a)
    h = NumericProperty(b)
    def on_enter(self, **kwargs):
        self.socketIP = '192.168.43.94'
        s = socket.socket()
        s.connect((self.socketIP,3335))
        s.send ('calibrate'.encode())
        if s.recv(1024).decode("ascii") == "step":
            s.close()
        
        self.manager.current = "home"

class Button(ButtonBehavior,Widget):
    pass

class Cal(App):
    Builder.load_file("kv/calibrate.kv")
    def build(self):
        
        return Calibrate()

if __name__ == '__main__':
    Cal().run()

