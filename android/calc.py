from kivy.app import App

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.config import Config

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button 
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.event import EventDispatcher
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ReferenceListProperty


class CalculatorWidget(Screen):
    [calc_w,calc_h] = Window.size
    loc_x = 0
    loc_y = 0
    
    int_button_font_size = 4

    center_x = NumericProperty(loc_x)
    center_y = NumericProperty(loc_y)
    calc_width = NumericProperty(calc_w)
    calc_height = NumericProperty(calc_h)

    

    def calc_error(self, error, calc_entry):
        self.ids.calc.text = 'error !'

    def calculate(self, *args):
        print (self.ids)
        calc_entry = self.ids.calc.text 
        if calc_entry != '':
            if calc_entry[0] in '1234567890-+':
                try:
                    ans = str(eval(calc_entry))
                    self.ids.calc.text = ans
                except Exception as error:
                    self.calc_error(error, calc_entry)
                    pass

    def delete(self, *args):
        self.ids.calc.text = self.ids.calc.text[:-1]

    def clear(self, *args):
        self.ids.calc.text = ''

    def switch(self, *args):
        calc_entry = self.ids.calc.text
        if calc_entry != '':
            if calc_entry[0] in '+1234567890':
                self.ids.calc.text = '-' + calc_entry
            if calc_entry[0] == '-':
                self.ids.calc.text = calc_entry[1:]

class Button(ButtonBehavior,Widget):
    pass

class CalculatorApp(App):
    def build(self):
        Builder.load_file("kv/Calculator.kv")
        return CalculatorWidget()

if __name__ == '__main__':
    CalculatorApp().run()
