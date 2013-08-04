import sys,os,time
import cPickle as p
from datetime import date, timedelta, datetime

YR=time.strftime('%Y')#'2013'
MONTHS=['January', 'February', 'March', 'April', 'May', 'June',\
	'July', 'August', 'September', 'October', 'November', 'December']
SMONTHS=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
DAYS=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
SDAYS=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

def printCurrency(n):
    """Reimplement locale.currency """
    if type(n)!=float: n=float(n)
    n=round(n, 2)
    s=str(n)
    #case: n is int
    #if n%1==0: return '$'+s+'.00'
    tail=s[s.find('.')+1:]
    if len(tail)==1: return '$'+s+'0'
    else: return '$'+s
    

def findDay(day):
    assert day in DAYS, "wtf man"
    """Given that day is a day of the week, find the most recent day, in the form of a datetime object"""
    #myday=time.localtime()
    l=getTime(7)
    for date in l:
        if date.strftime('%A')==day: return date
    else: return date.today()

def rmday(d, l):
    """d is the dict. l a list of strings. It can either be ['Weekday'], ['Month', 'Date'],
    ['Month', 'Date', 'Year']. Entirely remove the day from the record"""
    #assert l[0] in DAYS or l[0]+' '+l[1] in d.keys() or l[0]+' 0'+l[1] in d.keys(), '\n\ncheck yo self'

    l[0]=l[0].title() 
    if l[0] in SMONTHS: l[0]=MONTHS[SMONTHS.index(l[0])]
    if l[0] in SDAYS: l[0]=DAYS[SDAYS.index(l[0])]

    if l[0] in MONTHS: del d[l[0]+' '+l[1]+' '+(l[2] if len(l)>2 else YR)]
    elif l[0] in DAYS: del d[findDay(l[0]).strftime('%B %d %Y')]
    else: raise KeyError()

def remove(d, l, name):
    """Remove entry name from the record. If the day is empty, remove it. l can either be ['Weekday'], ['Month', 'Date'],
    ['Month', 'Date', 'Year'] """
    #assert l[0] in DAYS or l[0]+' '+l[1] in d.keys() or l[0]+' 0'+l[1] in d.keys(), '\n\ncheck yo self'

    l[0]=l[0].title()
    if l[0] in SMONTHS: l[0]=MONTHS[SMONTHS.index(l[0])]
    if l[0] in SDAYS: l[0]=DAYS[SDAYS.index(l[0])]
    l=[st.title() for st in l]
    if l[0] in MONTHS:
        x=date(int(l[2] if len(l)>2 else YR), int(MONTHS.index(l[0]))+1, int(l[1]))
    elif l[0] in DAYS:
        x=findDay(l[0])
    else: raise KeyError()

    t=list(d[x.strftime('%B %d %Y')])
    found=False
    for item in t:
        if item[item.find(';')+2:item.rfind(':')].title()==name.title():
            t.remove(item)
            found=True
            break
    if not found: raise ValueError()
    if len(t)==0: del d[x.strftime('%B %d %Y')]
    else: d[x.strftime('%B %d %Y')]=tuple(t)
    
def getTime(j):
    """Return a list of datetime objects representing j days back from today

    REALLY IMPORTANT!!!!!!!!!!!!
    DOES NOT WORK!!!!!!!!!!!!!!
    GETS TO DAY 0 AND THEN RAISES AN ERROR!!!!!!!!!!
    """
    
    l=[]
    day=date.today()
    for i in range(j):
        l.append(day)
        day-=timedelta(1)
    l.reverse()
    return l
            

def leapyr(n):
    if n % 400 == 0:
        return True
    if n % 100 == 0:
        return False
    if n % 4 == 0:
        return True
    else:
        return False
    
def _printWkdays():
    """Print the days of the week. Testing purposes only."""
    l=getTime(7)
    for day in l:
        print time.strftime('%A %B %d %Y',day)
    print

def printData(data, cat=False):
    """Print the data with pretty formatting. Eg:
    Monday, July 22
       coffee: 2.11
       ...
    Print the year as well if it's not this year.
    """
    s=''
    for d in data:
        s+= d[0].strftime('%A, %B %d')+'\n' if d[0].strftime('%Y')==YR else d[0].strftime('%A, %B %d %Y')+'\n'
        for i in range(len(d[1])):
            c=d[1][i].split(';')[0]
            c='('+c+') '
            s+= '   '+(c if cat else '')+d[1][i][d[1][i].find(';')+2:d[1][i].rfind(':')].title()+\
                ': '+printCurrency(d[1][i][d[1][i].rfind(':')+2:])+(' | ' if i!=(len(d[1])-1) else '')
        s+='\n'
    s+='.. _bottom:'
    s+='\n'
    return s

def printDay(d, day, cat=False):
    """Print the given day with pretty formatting. """
    data=getData(d)
    day[0]=day[0].title()
    if day[0] in SMONTHS: day[0]=MONTHS[SMONTHS.index(day[0])]
    if day[0] in SDAYS: day[0]=DAYS[SDAYS.index(day[0])]

    if day[0] in DAYS:
        s=findDay(day[0]).strftime('%B %d %Y')
        spl=s.split(' ')
        x=date(int(spl[2]), int(MONTHS.index(spl[0]))+1, int(spl[1]))
    else:
        #s=day[0]+' '+day[1]+' '+(day[2] if len(day)>2 else YR)
        x=date(int(day[2] if len(day)>2 else YR), int(MONTHS.index(day[0]))+1, int(day[1]))
    
    data=[da for da in data if da[0]==x]
    if len(data)==0: raise KeyError()
    return printData(data)

def printItem(d, item, ndays):
    """Print all days in which an item occurs, and the occurances of that item.
    This implementation is really nasty, but it works."""
    data=getData(d)
    if ndays>0: data=[x for x in data if x[0] in getTime(ndays)]
    for thing in data:# thing: (datetime, (costs))
        for cost in thing[1]:
            if cost.split(' ')[0][:-1]==item:
                print thing[0].strftime('%A, %B %d')
                for c in thing[1]:
                    if c.split(' ')[0][:-1]==item:
                        print '   '+c[c.find(';')+2:]

def sumItem(d, item, ndays=-1):
    """Sum all expenses for a certain item and return it as a float.
    l is either [item], or [-w, item]"""
    data=getData(d)
    if ndays>0: data=[x for x in data if x[0] in getTime(ndays)]
    res=0.0
    for t in data:
        for cost in t[1]:
            s=cost[cost.find(';')+2:cost.find(':')].title()
            if s==item.title():
                res+=float(cost[cost.rfind(':')+2:])
    return printCurrency(res)

def getD():
    return p.load(open('/home/dan/.config/cost/cost_save', 'rb'))
   
def getData(d):
    """Take the dict. Return a really compelex data structure of the form:
    [(datetime,(costs...)), ...], where datetime is a datetime object.
    The list is sorted by date."""
    data = [(datetime.strptime(k, '%B %d %Y').date(), v) 
        for k, v in d.items()]
    data.sort()
    return data

def printAll(d, cat):
    data=getData(d)
    data.reverse()
    s=printData(data, cat)
    return s

def printTime(d, ndays, cat):
    l=getTime(ndays)    
    data=getData(d)
    data=[d for d in data if d[0] in l]
    printData(data, cat)

def printWk(d, cat):
    printTime(d, 7, cat)

def sumAll(d):
    data=getData(d)
    res=0
    for d in data:
        for cost in d[1]:
            res+=float(cost[cost.rfind(':')+2:])
    return res

def sumTime(d, ndays=-1):
    data=getData(d)
    l=getTime(ndays)
    if ndays>0: data=[d for d in data if d[0] in l]
    res=0
    for d in data:
        for cost in d[1]:
            res+=float(cost[cost.rfind(':')+2:])
    return printCurrency(res)

def addComplete(d, l):
    """Here be over-wrought user input parsing"""
    l[0]=l[0].title()
    if l[0] in SMONTHS: l[0]=MONTHS[SMONTHS.index(l[0])]
    if l[0] in SDAYS: l[0]=DAYS[SDAYS.index(l[0])]
    l=[st.title() for st in l]
    assert '' not in l
    if l[0] in MONTHS:
        if len(l)==6: # year and category given
            herp=int(l[2]); herp=int(l[1])
            herp=float(l[4])
            herp=date(int(l[2]), int(MONTHS.index(l[0]))+1, int(l[1]))
            addRetro(d, l[0], l[1], l[3].title(), l[4], l[2], l[5].title())
        elif len(l)==5:
            # year or category given
            try: # year given
                y=int(l[2]) # see if it's a valid year. If not, assume it's an item
                y=str(y)
                category=raw_input("Type the category of this item (hit enter to put it in Misc.)\n")
                herp=date(int(y), int(MONTHS.index(l[0]))+1, int(l[1]))
                addRetro(d, l[0], l[1], l[3].title(), l[4], y, category.title() if category!='' else 'Misc.')
            except ValueError: #category given
                herp=date(int(YR), int(MONTHS.index(l[0]))+1, int(l[1]))
                addRetro(d, l[0], l[1], l[2].title(), l[3], YR, l[4].title())
        elif len(l)==4: # neither year nor category given
            herp=date(int(YR), int(MONTHS.index(l[0]))+1, int(l[1]))
            category=raw_input("Type the category of this item (hit enter to put it in Misc.)\n")
            addRetro(d, l[0], l[1], l[2].title(), l[3], YR, category.title() if category!='' else 'Misc.')
        else:
            raise Exception()
    elif l[0] in DAYS:
        day=findDay(l[0]).strftime('%B %d %Y').split(' ')
        if len(l)==3:
            category=raw_input("Type the category of this item (hit enter to put it in Misc.)\n")
            addRetro(d, day[0], day[1], l[1].title(), l[2], day[2], category.title() if category!='' else 'Misc.')
        elif len(l)==4:
            addRetro(d, day[0], day[1], l[1].title(), l[2], day[2], l[3].title())
        else:
            raise Exception()

    else:
        if len(l)==2:
            category=raw_input("Type the category of this item (hit enter to put it in Misc.)\n")
            addCost(d, l[0].title(), l[1], category.title() if category!='' else 'Misc.')
        elif len(l)==3:
            addCost(d, l[0].title(), l[1], l[2].title())
        else: 
            raise Exception()

def addRetro(d, mon, date, name, price, year, cat):
    s=mon+' '+date+' '+year
    if s not in d.keys():
        d[s]=(cat+'; '+name+': '+price,)
    else:
        d[s]=tuple(list(d[s])+[cat+'; '+name+': '+price])
        
def addCost(d, name, price, cat='Misc.'):
    if today() not in d.keys():
        d[today()]=(cat+'; '+name+': '+price,)
    else:
        d[today()]=tuple(list(d[today()])+[cat+'; '+name+': '+price])
    
def today():
    return time.strftime('%B %d %Y')

def mkPickle():
    p.dump({}, open(fName, 'wb'))

def startup():
    global fName
    fName=os.path.dirname(os.path.realpath(__file__))
    fName+='/' if os.name=='posix' else '\\'
    fName+='.cost_save'

def fixPickle():
    fName='/home/dan/cost/.cost_save'
    d=p.load(open(fName,'rb'))
    for day in d:
        l=[]
        for c in d[day]:
            cat=raw_input("What category is entry "+c.split(':')[0]+'?\n')
            l.append(cat+'; '+c)
        d[day]=tuple(l)
    print d
    yn=raw_input("should I save this (y/N)?\n")
    if yn.lower()=='y': p.dump(d, open(fName, 'wb'))

def getCatSet(d, ndays=-1):
    """Return a set of the categories present in d """
    s=set()
    data=getData(d)
    if ndays!=-1:
        l=getTime(ndays)
        data=[x for x in data if x[0] in l]
    for t in data:
        for cost in t[1]:
            s.add(cost.split(';')[0].title())
    return s
        
def sumCat(d, cat, ndays=-1):
    """Return the sum of all expenses in category cat ndays back from today.
    If ndays is -1, sum over all time"""
    res=0.0
    data=getData(d)
    if ndays!=-1:
        l=getTime(ndays)
        data=[x for x in data if x[0] in l]
    for t in data:
        for cost in t[1]:
            if cost.split(';')[0].title()==cat:
                res+=float(cost.split(' ')[-1])
    return res
                
def breakdown(d, ndays=-1, obj=None):
    print 'called'
    tot=float(sumTime(d, ndays)[1:]) if ndays>0 else sumAll(d)
    s=getCatSet(d, ndays)
    s=list(s)
    l=[]
    st=''
    for el in s:
        l.append(float(sumCat(d, el, ndays)))
    for i in range(len(s)):
        st+= '   '+s[i]+' constituted '+str(round((l[i]/tot*100),2))+'% ('+printCurrency(l[i])+')\n'
    if obj is not None: obj.text=st
    else: return st
        
def parseOpts(av):
    """Parse options into a set of characters """
    se=set()
    for s in av:
        if s[0]=='-':
            s=s[1:]
            for char in s:
                se.add(char)
    
    return se

def getTopNames(d, price=False, ndays=-1):
    """Return a list of the top five costs in d, if d is longer than 5, otherwise all of d
    If price, sort by price, otherwise, sort by most common."""
    dic={}
    data=getData(d)
    if ndays>0: data=[d for d in data if d[0] in getTime(ndays)]
    for t in data:
        for cost in t[1]:
            name=cost[cost.find(';')+2:cost.rfind(':')].title()
            nPrice=float(cost[cost.rfind(':')+2:])
            if name not in dic.keys(): dic[name]=nPrice if price else 1 
            else: dic[name]+=nPrice if price else 1
    l=[]
    for i in range(5 if len(dic)>=5 else len(dic)):
        mName=getMaxInDict(dic)
        l.append(mName)
        del dic[mName]
    return l

def getMaxInDict(dic):
    m=0; mName=''
    for name in dic.keys():
        if dic[name]>m:
            mName=name
            m=dic[name]
    return mName


def getTopCats(d, ndays=-1):
    data=getData(d)
    dic={}
    
    if ndays>0: data=[d for d in data if d[0] in getTime(ndays)]
    for t in data:
        for cost in t[1]:
            cat=cost[:cost.find(';')].title()
            nPrice=float(cost[cost.rfind(':')+2:])
            if cat not in dic.keys(): dic[cat]=nPrice
            else: dic[cat]+=nPrice
    l=[]
    for i in range(4 if len(dic)>=4 else len(dic)):
        mName=getMaxInDict(dic)
        l.append(mName)
        del dic[mName]
    return l

def getTopCatPercents(d, ndays=-1):
    tot=sumAll(d)
    dic={}
    s=0
    for el in getTopCats(d, ndays):
        sc=sumCat(d, el)
        dic[el]=sc/tot
        s+=sc
    if s!=tot:
        dic['Other']=s/tot
    return dic

def getMostRecentCost(d, name):
    data=getData(d)
    data.reverse()
    for d in data:
        for cost in d[1]:
            n=cost[cost.find(';')+2:cost.rfind(':')].title()
            if n==name.title(): return cost
    return None
