import kivy
kivy.require('1.0.6')

from glob import glob
from random import randint
from os.path import join, dirname
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.uix.button import Button 
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView

class Picture(Scatter):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''

    source = StringProperty(None)
class backButton(Button):
    pass

class Pictures(Screen):

    def __init__(self,**kwargs):
        super(Pictures,self).__init__(**kwargs)
        # the root is created in pictures.kv
    def show(self,folder_name):
        
        curdir = dirname(__file__)
        self.ids.frame.add_widget(backButton())
        for filename in glob(join(curdir, 'images',folder_name, '*')):
            try:
                # load the image
                picture = Picture(source=filename, rotation=randint(-30, 30))
                # add to the main field
                self.ids.frame.add_widget(picture)
            except Exception as e:
                print (e)
    
    def on_pause(self):
        return True


if __name__ == '__main__':
    PicturesApp().run()