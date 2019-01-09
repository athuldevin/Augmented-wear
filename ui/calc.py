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
from kivy.properties import NumericProperty, ReferenceListProperty


class CalculatorWidget(BoxLayout):
    int_button_width = 550
    int_button_height = 300
    int_button_font_size = 40

    button_width = NumericProperty(int_button_width)
    button_height = NumericProperty(int_button_height)
    button_font_size = NumericProperty(int_button_font_size)

    Window.size = (int_button_width , int_button_height )

    def calc_error(self, error, calc_entry):
        content = BoxLayout(orientation='vertical')
        scrollview = ScrollView()

        close_popup = Button(text='Close this popup')
        error_message = Label(text=str(error))

        scrollview.add_widget(error_message)
        content.add_widget(scrollview)
        content.add_widget(close_popup)

        popup = Popup(title='An error occured',
            content=content, size_hint=(.8, .8))

        close_popup.bind(on_release=popup.dismiss)
        popup.open()

    def calculate(self, *args):
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
