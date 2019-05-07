from kivy.uix.screenmanager import Screen
import socket
import datetime
import random 
import sys,os
class Camera(Screen):
    def on_enter(self, **kwargs):
        self.socketIP = '192.168.43.94'
        s = socket.socket()
        s.connect((self.socketIP,3335))
        s.send ('capture'.encode())
        curdir = os.path.dirname(__file__)
        curdir=os.path.join(curdir, 'images/captures/')
        print (curdir)
        f = open(str(curdir)+'image'+ str(datetime.date.today())+str(random.randint(1, 100))+".png",'wb') # Open in binary
        l = s.recv(1024)
        while (l):
            f.write(l)
            l = s.recv(1024)
        f.close()
        s.close()
        self.manager.current = "home"