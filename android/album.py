import kivy

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
  
class Folder(ButtonBehavior, Image):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''

    folder_name = StringProperty(None)
    source = StringProperty(None)
    def __init__(self, **kwargs):
        super(Folder, self).__init__(**kwargs)
    def switch(self):
        
        self.parent.parent.parent.manager.get_screen('pictures').ids.frame.clear_widgets()
        self.parent.parent.parent.manager.get_screen('pictures').show(self.folder_name)
        self.parent.parent.parent.manager.current="pictures"
        
        

class Album(Screen):

    def __init__(self,**kwargs):
        super(Album,self).__init__(**kwargs)
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
        curdir = os.path.dirname(__file__)
        curdir=os.path.join(curdir, 'images')
        for path, subdirs, files in os.walk(curdir):
            for name in subdirs:
               
                for filename in glob(os.path.join(curdir,name, '*')):
                    try:
                        # load the image
                        folder = Folder(folder_name=name,source=filename)
                        self.ids.content.add_widget(folder)
                        # add to the main field
                        break
                    except Exception as e:
                        print (e)
                
    def on_pause(self):
        return True
  


if __name__ == '__main__':
    AlbumApp().run()