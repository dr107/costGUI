from kivy.app import App
from kivy.utils import platform
from kivy.uix.screenmanager import *
from screenz import *
import cPickle as p
from os.path import isfile
from kivy.core.window import Window
from kivy.uix.widget import WidgetException
"""
TODO:
    Make popups stored in App.popup
    Make every screen have a prev and prevTrans
"""


class MyScreenManager(ScreenManager):
    """ 
    The idea is to subclass screenmanager in order to be able to intelligently go 
    backwards using the android back button. We'll see how this winds up working.
    prev is a list of strings 
    """
    def __init__(self):
        super(MyScreenManager,self).__init__()
    def back(self):
        cur=self.current_screen; prev=self.get_screen(cur.prev);
        #print 'current screen: '+cur.name+' whose transition state is: '+str(cur.transition_progress)
        #print 'prev screen: '+prev.name+' whose transition state is: '+str(prev.transition_progress)

        if cur.transition_progress<1: 
            return
        if self.current_screen.name=='help':
            self.current_screen.reset()
        self.transition=SlideTransition(direction=self.current_screen.prevTrans)
        self.current=self.current_screen.prev
class CostApp(App):
    d=None
    fName=None
    man=None
    firstRun=False

    def firstRunOp(self):
        dump(load(open('cost_save_example', 'rb')), open(self.fName, 'wb'))
        self.firstRun=True

    def build(self):
        # back button stuff
        self.bind(on_start=self.post_build_init)
        
        #other stuff
        self.firstRun=False
        self.on_pause=self.save
        self.on_stop=self.save
        self.fName=self.user_data_dir+'/cost_save'
        if not isfile(self.fName): self.firstRunOp()
        self.d=p.load(open(self.fName, 'rb'))
        sm=MyScreenManager()
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
        self.popup=None
        return sm

    def post_build_init(self, *args):
        if platform() == 'android':
            import android
            android.map_key(android.KEYCODE_BACK, 1001)

        win = Window
        win.bind(on_keyboard=self.my_key_handler)

    def my_key_handler(self, window, keycode1, keycode2, text, modifiers):
        if keycode1 in [27, 1001]:
            if self.popup is None:
                self.man.back()
            else:
                self.popup.dismiss()
            return True
        return False

    def save(self):
        dump(self.d, open(self.fName,'wb'))

if __name__=='__main__':
    CostApp().run()
