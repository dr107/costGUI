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
from kivy.graphics import *
from kivy.lang import Builder
from kivy.uix.popup import Popup
from functools import partial
from cost import *
from cPickle import load, dump
from datetime import *
from os.path import isfile
from functools import partial

class QuickAddScreen(Screen):
    qab=ObjectProperty()
    sub_btn=ObjectProperty()
    det_btn=ObjectProperty()
    back_btn=ObjectProperty()

class RMScreen(Screen):
    log=ObjectProperty()
    lab=ObjectProperty()
    date_bx=ObjectProperty()
    day_btn=ObjectProperty()
    ent_btn=ObjectProperty()
    cancel=ObjectProperty()

    def dayBtnPush(self, obj):
        if not self.date_bx.nameMode: self.removeDay(obj)
    def entBtnPush(self, obj):
        if not self.date_bx.nameMode: self.removeEntry(obj)

    def __init__(self, **kwargs):
        super(RMScreen, self).__init__(**kwargs)
        self.day_btn.bind(on_release=self.dayBtnPush)
        self.ent_btn.bind(on_release=self.entBtnPush)
        self.genlog()

    def reset(self):
        self.date_bx.text=date.today().strftime('%B %d %Y')
        self.genlog()
        self.lab.text="What day has the problem?\n"+\
            "(RET to delete entire day)"
        self.date_bx.nameMode=False
        
    def genlog(self):
        self.log.text=printAll(App.get_running_app().d, True)

    def removeEntry(self, obj):
        """Change display to 1 day, clear text in, change label to ask which entry """
        self.date_bx.l=str(self.date_bx.text).split(' ')
        try:
            self.log.text=printDay(App.get_running_app().d, self.date_bx.l, False)
            self.lab.text='What is the name of the entry you wish to remove?'+\
                '\n(RET to submit)'
            self.date_bx.nameMode=True
            self.date_bx.text=''

        except KeyError, ValueError:
            self.dayNotFound()

    
    def actuallyRemoveEntry(self, l, text):
        l=[s.title() for s in l]
        try:
            remove(App.get_running_app().d, l, text)
            self.rmSuccess(True)
            self.reset()
        except KeyError:
            self.dayNotFound()
        except ValueError:
            self.entryNotFound()

    def entryNotFound(self):
        pu=Popup(title="Failure..", size_hint=(1,.75))
        blo=BoxLayout(orientation='vertical', spacing="5dp")
        lab=Label(text_size=pu.size, text='There is no record for that entry\n'+\
                                 'Check your input', valign='middle', halign='center')
        lab.bind(size=lab.setter('text_size')) 
        lab.size_hint=(1,1)        
        blo.add_widget(lab)
        backBtn=Button(text='Go Back', size_hint=(1,.33))
        backBtn.bind(on_press=self.toHelp, on_release=pu.dismiss)
        blo.add_widget(backBtn)
        stayBtn=Button(text='Stay Here', size_hint=(1,.33))
        stayBtn.bind(on_release=pu.dismiss)
        blo.add_widget(stayBtn)
        pu.content=blo
        pu.on_dismiss=self.reset
        pu.open()

    
    def dayNotFound(self):
        pu=Popup(title="Failure..", size_hint=(1,.75))
        blo=BoxLayout(orientation='vertical', spacing="5dp")
        lab=Label(text_size=pu.size, text='There is no record for that day\n'+\
                      'Check Help->Input Help for acceptable date formats', halign='center', valign='middle')
        lab.bind(size=lab.setter('text_size')) 
        lab.size_hint=(1,1)
        blo.add_widget(lab)
        backBtn=Button(text='Go Back', size_hint=(1,.33))
        backBtn.bind(on_press=self.toHelp, on_release=pu.dismiss)
        blo.add_widget(backBtn)
        stayBtn=Button(text='Stay Here', size_hint=(1,.33))
        stayBtn.bind(on_release=pu.dismiss)
        blo.add_widget(stayBtn)
        pu.content=blo
        pu.on_dismiss=self.reset
        pu.open()


    def rmSuccess(self, entry=False):
        pu=Popup(title="Success!", size_hint=(1,.75))
        blo=BoxLayout(orientation='vertical', spacing="5dp")
        lab=Label(text=('Day' if not entry else 'Entry')+\
                             ' removed successfully',halign='center', valign='middle')
        lab.bind(size=lab.setter('text_size')) 
        lab.size_hint=(1,1)
        blo.add_widget(lab)
        backBtn=Button(text='Go Back', size_hint=(1,.33))
        backBtn.bind(on_press=self.toHelp, on_release=pu.dismiss)
        blo.add_widget(backBtn)
        stayBtn=Button(text='Stay Here', size_hint=(1,.33))
        stayBtn.bind(on_release=pu.dismiss)
        blo.add_widget(stayBtn)
        pu.content=blo
        pu.on_dismiss=self.reset
        pu.open()

    def removeDay(self, obj=None):
        l=str(self.date_bx.text).split(' ')
        try:
            rmday(App.get_running_app().d, l)
            dump(App.get_running_app().d, open(App.get_running_app().fName, 'wb'))
            self.genlog()
            self.rmSuccess()
        except KeyError:
            self.dayNotFound()

    def toHelp(self, obj):
        self.reset()
        self.manager.transition=SlideTransition(direction="down")
        self.manager.current='help'

class InputScreen(Screen):
    doc=ObjectProperty()
    def __init__(self, **kwargs):
        super(InputScreen, self).__init__(**kwargs)
        self.doc.source='help.rst'
    def toHelp(self, obj=None):
        self.manager.transition=SlideTransition(direction="right")
        self.manager.current='help'
    def toMain(self, obj=None):
        self.manager.transition=SlideTransition(direction="down")
        self.manager.current='main'


class BkdwnScreen(Screen):
    rst=ObjectProperty()
    mo_btn=ObjectProperty()
    wk_btn=ObjectProperty()
    at_btn=ObjectProperty()
    def __init__(self, **kwargs):
        super(BkdwnScreen, self).__init__(**kwargs)
        self.rst.text=breakdown(App.get_running_app().d)
        self.mo_btn.on_release=partial(breakdown,\
                                           App.get_running_app().d, 30, self.rst)
        self.wk_btn.on_release=partial(breakdown,\
                                           App.get_running_app().d, 7, self.rst)
        self.at_btn.on_release=partial(breakdown,\
                                           App.get_running_app().d, -1, self.rst)
class TotScreen(Screen):
    title=ObjectProperty()
    tots=ObjectProperty()
    top_title=ObjectProperty()
    tops=ObjectProperty()
    grd=ObjectProperty()
    wk_btn=ObjectProperty()
    mo_btn=ObjectProperty()
    at_btn=ObjectProperty()

    def __init__(self, **kwargs):
        super(TotScreen, self).__init__(**kwargs)
        self.displayATTops()
        self.tots.text=self.displayTots()

    def displayATTops(self):
        self.top_title.text='Top Items (All Time)'
        d=App.get_running_app().d
        l=getTopNames(d, True)
        s=''
        for i in range(len(l)):
            s+=str(i+1)+'. '+l[i]+' ('+sumItem(d,l[i])+')'+'\n'
        self.tops.text= s

    def displayMOTops(self):
        self.top_title.text='Top Items (This Month)'
        d=App.get_running_app().d
        l=getTopNames(d, True, 30)
        s=''
        for i in range(len(l)):
            s+=str(i+1)+'. '+l[i]+' ('+sumItem(d,l[i], 30)+')'+'\n'
        self.tops.text=s

    def displayWKTops(self):
        self.top_title.text='Top Items (This Week)'
        d=App.get_running_app().d
        l=getTopNames(d, True, 7)
        s=''
        for i in range(len(l)):
            s+=str(i+1)+'. '+l[i]+' ('+sumItem(d,l[i],7)+')'+'\n'
        self.tops.text=s
        
    def displayTots(self):
        d=App.get_running_app().d
        s='Daily total '+sumTime(d, 1)+'\n'
        s+='Weekly total '+sumTime(d, 7)+'\n'
        s+='Monthly total '+sumTime(d, 30)
        return s

    def itemSum(self):
        textl=['herp'] # stupid trick
        pu=Popup(title='Which?', size_hint=(1,.75))
        lay=BoxLayout(orientation='vertical')
        lab=Label(text_size=pu.size, text='Which item do you want to get totals for?', halign='center', valign='middle')
        lab.bind(size=lab.setter('text_size')) 
        lab.size_hint=(1,1)
        txi=SumNameIn(pu, multiline=False)
        btn=Button(text='Submit', on_release=pu.dismiss)
        lay.add_widget(lab)
        lay.add_widget(txi)
        lay.add_widget(btn)
        pu.content=lay
        pu.on_dismiss=lambda: self.actuallyItemSum(txi.text)
        pu.open()
        
    def actuallyItemSum(self, name):
        t=float(sumItem(App.get_running_app().d, name)[1:])
        s='Amount spent on '+name+' this week: '+sumItem(App.get_running_app().d, name, 7)+'\n'
        s+='This month: '+sumItem(App.get_running_app().d, name, 30)+'\n'
        s+='All time: '+sumItem(App.get_running_app().d, name)+'\n'
        pu=Popup(title='Totals', size_hint=(1,.75))
        lay=BoxLayout(orientation='vertical')
        lab=Label(text_size=pu.size, text=(s if t>0 else 'There is no record of any entry with that name.\nTry again' ),\
                      halign='center',valign='middle')
        lab.bind(size=lab.setter('text_size')) 
        lab.size_hint=(1,1)
        btn=Button(text='OK', on_release=pu.dismiss, size_hint_y=.3)
        lay.add_widget(lab)
        lay.add_widget(btn)
        pu.content=lay
        pu.open()
        

    def reset(self):
        self.displayATTops()
        self.tots.text=self.displayTots()
    def gotoMain(self, obj):
        self.manager.current='main'

class AddScreen(Screen):
    name_box=ObjectProperty()
    price_box=ObjectProperty()
    date_box=ObjectProperty()
    cat_box=ObjectProperty()
    save=ObjectProperty()

    def print_data(self):
        d=App.get_running_app().d
        l=[]
        l+=self.date_box.text.split(' '); self.date_box.text=date.today().strftime('%B %d %Y')
        l+=[str(self.name_box.text.strip())]; self.name_box.text=''
        l+=[str(self.price_box.text.strip())]; self.price_box.text=''
        l+=[str(self.cat_box.text.strip()) if str(self.cat_box.text.strip())!='' else 'Misc.']; self.cat_box.text=''
        try:
            addComplete(d,l)
            return True
        except:
            pu=Popup(title='Input Error', size_hint=(1,.75), auto_dismiss=False)
            label=Label(text_size=pu.size, 
                        text='Something seems to be wrong with your input.\nCheck help if you\'re unsure what\'s wrong.',
                        halign='center',valign='middle')
            label.bind(size=label.setter('text_size')) 
            label.size_hint=(1,1)
            disBtn=Button(text='OK', size_hint=(1,.4))
            disBtn.bind(on_release=lambda disBtn: pu.dismiss(disBtn))
            puLO=BoxLayout(orientation='vertical')
            puLO.add_widget(label); puLO.add_widget(disBtn);
            pu.content=puLO
            pu.open()
            return False

class ViewScreen(Screen):
    log=ObjectProperty()
    check=ObjectProperty()
    def __init__(self,**kwargs):
        super(ViewScreen,self).__init__(**kwargs)
        self.check.bind(active=self.on_checkbox_activate)
    def reload(self): 
        self.log.text=printAll(App.get_running_app().d, self.check.active)
    def on_checkbox_activate(self, cb, val):
        self.reload()
    
class AnlzScreen(Screen):
    pass

class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen,self).__init__(**kwargs)
        if App.get_running_app().firstRun: Clock.schedule_once(self.firstRun, .1)

    def firstRun(self, obj):
        pu=Popup(size_hint=(1, .6), title='Welcome to Cost!')
        lo=BoxLayout(orientation='vertical')
        lab=Label(text="Hi! Cost is a program designed to help you track and "+\
        "understand where your money is going. We've provided you with a one-month "+\
        "example record so that you can explore some of the analysis features. "+\
        "When you think you get the idea go to Help->Clear Record from the main screen "+\
        "and hit OK at the prompt. Enjoy, and remember that this tool will only help you "
        "if you record every expense, no matter how minor. Those $2.11 coffees add up ;)", valign='middle', halign='center')
        lab.bind(size=lab.setter('text_size')) 
        lab.size_hint=(1,1)
        btn=Button(text='Got it', on_release=pu.dismiss, size_hint_y=.25)
        lo.add_widget(lab)
        lo.add_widget(btn)
        pu.content=lo
        lab.text_size=lab.size
        print lab.size
        pu.open()
        
    
class HelpScreen(Screen):
    clearPU=None
    def clearRecord(self):
        s ="Are you sure about this? This action will remove your"
        s+="record as it is. It will be saved as /sdcard/cost/cost_backup."
        s+="If you want to restore it, you will have to rename that file to"
        s+="cost_save manually, and as of now there is no way to merge records"
        s+="Of course, if you're just removing the example and want to get"
        s+="started, go right ahead"
        pu=Popup(size_hint=(.8, .6), title='Are you sure?')
        self.clearPU=pu
        lo=BoxLayout(orientation='vertical')
        lab=Label(text=s,halign='center',valign='middle')
        btn1=Button(text='Do it', on_release=self.doIt, size_hint_y=.25)
        btn2=Button(text='On second thought...', on_release=pu.dismiss, size_hint_y=.25)
        lo.add_widget(lab)
        lo.add_widget(btn1)
        lo.add_widget(btn2)
        pu.content=lo
        pu.open()
    
    def doIt(self, obj):
        dump(App.get_running_app().d, open(App.get_running_app().user_data_dir+'/cost_backup', 'wb'))
        App.get_running_app().d={}
        App.get_running_app().save()
        self.clearPU.dismiss()
