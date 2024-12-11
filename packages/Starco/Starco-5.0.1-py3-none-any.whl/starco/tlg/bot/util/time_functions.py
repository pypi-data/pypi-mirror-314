from datetime import datetime,timedelta
import pytz
from jdatetime import datetime as jdt


def get_timestamp(str_input='',sec=None,min=None,hour=None,day=None,month=None,m_sec=None,ms = True,tehran=True):
    ''' 
        
        if inp > 0 replace with inp else do decrease
        inputs = month , day , sec
        
        
        str_input:now , today , yesterday,this_month,last_month
        return ts
    '''
    
    if tehran:
        tz = pytz.timezone('Asia/Tehran')
        now = datetime.now(tz=tz)
    else:now = (datetime.now(pytz.utc))

    if str_input=='today':
        m_sec=0
        sec=0
        min=0
        hour=0
    elif str_input=='yesterday':
        m_sec=0
        sec=0
        min=0
        hour=0
        day=-1
    
    elif str_input=='this_month':
        m_sec=0
        sec=0
        min=0
        hour=0
        day=1
    elif str_input=='last_month':
        m_sec=0
        sec=0
        min=0
        hour=0
        day=1
        month=now.month-1
        year = now.year
        if month==0:
            year-=1
            month = 12
    
    if m_sec!=None:
        if m_sec<0:
            now = now-timedelta(milliseconds=abs(m_sec))
        else:
            now = now.replace(microsecond=m_sec)

    if sec!=None:
        if sec<0:
            now = now-timedelta(seconds=abs(sec))
        else:
            now = now.replace(second = sec)
    
    if min!=None:
        if min<0:
            now = now-timedelta(minutes=abs(min))
        else:
            now = now.replace(minute=min)
            
    if hour!=None:
        if hour<0:
            now = now-timedelta(hours=abs(hour))
        else:
            now = now.replace(hour = hour)
    
    if day!=None:
        if day<0:
            now = now-timedelta(days=abs(day))
        else:
            now = now.replace(day = day)
       
    if month!=None:
        if month<0:
            now = now-timedelta(months=abs(month))
        else:
            now = now.replace(month = month,year=year)
    
        
    res = now.timestamp()
    if ms:
        res*=1000
    return int(res)

def convert_to_ms(ts):
    if len(str(ts))<13:
        return ts*1000
    return ts


def to_jalali(ts:int):
    '''
    return jalali datetime
    '''
    ts= int(convert_to_ms(ts)/1000)
    return jdt.fromtimestamp(ts)
