import kivy
import datetime
import random 
from glob import glob
from random import randint
import sys,os
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
  
class Fold(ButtonBehavior, Image):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''
    file_name = StringProperty(None)
    source = StringProperty(None)
    
    def __init__(self, **kwargs):
        super(Fold, self).__init__(**kwargs)
    def switch(self):
        
        #self.parent.parent.parent.manager.get_screen('paint').ids.frame.clear_widgets()
        self.parent.parent.parent.manager.get_screen('paint').show(self.file_name)
        self.parent.parent.parent.manager.current='paint'
        
        

class DrawBoard(Screen):

    def __init__(self,**kwargs):
        super(DrawBoard,self).__init__(**kwargs)
        # the root is created in pictures.kv
        '''
        curdir = os.path.dirname(__file__)
        for filename in glob(os.path.join(curdir, 'images', '*')):
            try:
                # load the image
                picture = Folder(source=filename)
                # add to the main field
                self.ids.content.add_widget(picture)
            except Exception as e:
                print(e)
        '''

        # get any files into images directory
        
            
    def on_pause(self):
        return True
    def on_enter(self):
        curdir = os.path.dirname(__file__)
        curdir=os.path.join(curdir, 'paint')
        fn = str(datetime.date.today())+str(random.randint(1, 100))+".png"
        cur = os.path.join(os.path.dirname(__file__),'p.png')
        folder = Fold(file_name=fn, source=cur)
        self.ids.content.add_widget(folder)
        
        for path, subdirs, files in os.walk(curdir):
            print (files)
            for i in files:
                print (i)
                filename = os.path.join(curdir, i)
                try:
                    # load the image
                    folder = Fold(file_name=i, source=filename)
                    print (filename, i)
                    self.ids.content.add_widget(folder)
                    # add to the main field
                    
                except Exception as e:
                    print (e)
    def on_leave(self):
        self.ids.content.clear_widgets()
        self.ids.content.add_widget(self.ids.a)
        self.ids.content.add_widget(self.ids.b)
        self.ids.content.add_widget(self.ids.c)
  


if __name__ == '__main__':
    AlbumApp().run()