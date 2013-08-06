from kivy.app import App
from kivy.uix.screenmanager import *
from screenz import *
import cPickle as p
from os.path import isfile
"""
more meaningless changes
TODO:
return for adding while in the category buffer
finish (implement buttons) and possibly re-align total screen
breakdowns (my body is SO FUCKING READY)
Intelligent guessing of categories (in both this and cmd versions)
Clean up code/prepare for release (icon, format UI better for a given platform etc).
Package into desktop (Win, OSX)
"""

class CostApp(App):
    d=None
    fName=None
    man=None
    firstRun=False

    def firstRunOp(self):
        dump(load(open('cost_save_example', 'rb')), open(self.fName, 'wb'))
        self.firstRun=True

    def build(self):
        self.firstRun=False
        self.on_pause=self.save
        self.on_stop=self.save
        self.fName=self.user_data_dir+'/cost_save'
        if not isfile(self.fName): self.firstRunOp()
        self.d=p.load(open(self.fName, 'rb'))
        sm=ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ViewScreen(name='view'))
        sm.add_widget(AddScreen(name='add'))
        sm.add_widget(AnlzScreen(name='anlz'))
        sm.add_widget(HelpScreen(name='help'))
        sm.add_widget(RMScreen(name='rm'))
        sm.add_widget(InputScreen(name='in'))
        sm.add_widget(BkdwnScreen(name='bkdwn'))
        sm.add_widget(TotScreen(name='tot'))
        sm.add_widget(QuickAddScreen(name='qadd'))
        self.man=sm
        return sm

    def save(self):
        dump(self.d, open(self.fName,'wb'))

if __name__=='__main__':
    CostApp().run()
