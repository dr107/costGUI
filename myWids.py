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
from kivy.uix.popup import Popup
from functools import partial
from cost import *
from cPickle import load, dump
from datetime import *
from os.path import isfile
from functools import partial

class MyPopUp(Popup):
    """Make popups update App.popup """
    def __init__(self,**kwargs):
        super(Popup,self).__init__(**kwargs)
        App.get_running_app().popup=self
    
    def dismiss(self,*largs,**kwargs):
        App.get_running_app().popup=None
        super(Popup,self).dismiss()

class QuickAddBox(TextInput):
    def __init__(self, **kwargs):
        super(QuickAddBox, self).__init__(**kwargs)
        self.on_touch_down=self.downClr


    def downClr(self, touch):
        if self.text=='Type the name of a previous entry..':
            self.text=''
            super(QuickAddBox, self).on_touch_down(touch)
        else:
            super(QuickAddBox, self).on_touch_down(touch)

    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        if self.text=='Type the name of a previous entry..':
            self.text=''
            super(QuickAddBox, self)._keyboard_on_key_down(
                window, keycode, text, modifiers)
            
        elif keycode[0]==13: self.addQuick(self.text)
        
        else:
            super(QuickAddBox, self)._keyboard_on_key_down(
                window, keycode, text, modifiers)
    def addQuick(self, item):
        self.text=''
        try:
            cost=getLastInstance(App.get_running_app().d, item)
            self.displaySuccess(cost)
        except ValueError:
            self.displayFailure()

    
    def logIt(self, l, obj=None):
        d=App.get_running_app().d
        addComplete(d, l)
        App.get_running_app().man.get_screen('view').refresh()
        self.text=''
        self.focus=False

    def displaySuccess(self, cost):
        cat=cost[:cost.find(';')].title()
        name=cost[cost.find(';')+2:cost.rfind(':')].title()
        price=cost[cost.rfind(':')+2:]
        l=[name, price, cat]
        pu=MyPopUp(title="Entry Found!", size_hint=(1,.75))
        blo=BoxLayout(orientation='vertical', spacing="5dp")
        lab=Label(text_size=pu.size, text='The following data were found:\n'+\
                  'Name: '+name+'\n'
              'Price: '+price+'\n'
              'Category: '+cat,valign='middle', halign='center')
        lab.bind(size=lab.setter('text_size')) 
        lab.size_hint=(1,1)        
        blo.add_widget(lab)
        backBtn=Button(text='Log it', size_hint=(1,.33))
        backBtn.bind(on_press=lambda obj: self.logIt(l), on_release=pu.dismiss)
        blo.add_widget(backBtn)
        stayBtn=Button(text='Nope', size_hint=(1,.33))
        stayBtn.bind(on_release=pu.dismiss)
        blo.add_widget(stayBtn)
        pu.content=blo
        pu.open()
        

    def displayFailure(self):
        pu=MyPopUp(title="Failure..", size_hint=(1,.75))
        blo=BoxLayout(orientation='vertical', spacing="5dp")
        lab=Label(text_size=pu.size, text='There are no entries with that name\n'+\
                      'Check your input, or use the normal add function',
                  valign='middle', halign='center'
                  )
        lab.bind(size=lab.setter('text_size')) 
        lab.size_hint=(1,1)        
        blo.add_widget(lab)
        stayBtn=Button(text='OK', size_hint=(1,.33))
        stayBtn.bind(on_release=pu.dismiss)
        blo.add_widget(stayBtn)
        pu.content=blo
        pu.open()
        



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
