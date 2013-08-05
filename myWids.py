from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.rst import RstDocument
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import *
#from kivy.graphics import *
#from kivy.lang import Builder
from kivy.uix.popup import Popup
from functools import partial
from cost import *
from cPickle import load, dump
from datetime import *
from os.path import isfile
from functools import partial

class CostTextInput(TextInput):
    next=ObjectProperty()
    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[0] == 9 or keycode[0]==13:  # 9 is the keycode for TAB
            self.next.focus = True
        else:
            super(CostTextInput, self)._keyboard_on_key_down(
                    window, keycode, text, modifiers)


class SumNameIn(TextInput):
    """Exists for the sole purpose of item sum """
    pu=None
    def __init__(self, pu=None,  **kwargs):
        super(SumNameIn, self).__init__(**kwargs)
        self.pu=pu
    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[0]==13:
            self.pu.dismiss()
        else:
            super(SumNameIn, self)._keyboard_on_key_down(window, keycode, text, modifiers)
            

class DateIn(TextInput):
    nameMode=False
    l=[]
    def __init__(self, **kwargs):
        super(DateIn, self).__init__(multiline=False,**kwargs)
    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        if self.nameMode and keycode[0]==13:
            rms=App.get_running_app().man.get_screen('rm')
            rms.actuallyRemoveEntry(self.l, self.text)
        elif not self.nameMode and keycode[0]==13:
            rms=App.get_running_app().man.get_screen('rm')
            rms.removeDay(self.l)
        else:
            super(DateIn, self)._keyboard_on_key_down(
                    window, keycode, text, modifiers)
