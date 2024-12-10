from ..base import Base
from ..classes import Conversation
from .enum import Pack,Node
from .filteres import match_btn,match_text
from telegram.ext import Filters
from .enum import *
from ..classes import Conversation
import telegram
from telegram.ext import Filters
import time
from functools import partial
from .filteres import *
from starco.utils import chunks

def Start(self:Conversation):
    
    def act(self:Conversation,*args):
        try:
            self.send(msg = 'start_pm',btns = self.menu_keys,get_text_setting=True)
        except Exception as e:print(e)
        return -1

    p = Pack()
    p.name = 'start'

    e1 = Node()
    e1.command = 'start'
    e1.command_filters = match_text('/start')
    e1.callback=act

    e2=Node()
    e2.pattern = self.check_inline_keyboards('/start',1)
    e2.callback = act
    p.entry=[e1]
    return p

def ForceJoinPack(self:Conversation,**kargs):
    p = Pack()
    get_text_setting =kargs.get('get_text_setting',False)
    p.name="force_join_pack"
    p.db_config = {'force_join': {'id': 0, 'title': '', 'channel_id': '', 'link': '','status':0},'users':{'force_check_ts':0,'force_check_staus':0}}
    
    e=Node()
    e.filters = ~ForceJoinFilter(self)
    def act(self:Conversation,*a):
        try:
            start_bot = self.splited_query_data()[0]
            if start_bot == 'start_bot':
                self.alert(self.text('join_alert_pm'))
                return -1
        except:
            pass
        btns = {}
        for i in self.db.do('force_join',condition=f"status={CONFIRMED}"):
            print(i)
            link = i['link']
            btns[i['title']] = link
            txt = self.get_text()
            if txt and  '/start' in txt:
                btns['start_bot'] =txt 
            else:btns['start_bot'] ='start_bot'
        self.send(msg='join_pm', btns = btns,col=1,get_text_setting=get_text_setting,close=False)
        return -2
    e.callback =act

    e1=Node()
    e1.pattern = self.force_join_inline_filter()
    e1.callback=act

    ch = Node()
    ch.pattern = self.check_inline_keyboards('start_bot',1)
    def act(self:Conversation,*a):
        do_force_join_del_pm(self)
        return -2

    ch.callback=act
    
    p.entry=[e,e1,ch]
    return p

def do_force_join_del_pm(self:Conversation):
    try:
        self.splited_query_data()[0]
        self.delete_message(self.get_msg_id())
    except:pass

def SharePhone(self:Conversation,**kargs):
    p = Pack()
    p.name = 'share_phone'
    get_text_setting =kargs.get('get_text_setting',False)

    e1=Node()
    e1.filters = SharePhoneFilter(self)
    def show_pm(self,*a):
        self.send('share_phone', [['share_phone']], share_phone=True,get_text_setting=get_text_setting)
        return -1
    e1.callback = show_pm

    e=Node()
    e.filters = Filters.contact
    def act(self:Conversation,*args):
        contact = self.update.effective_message.contact
        phone = contact.phone_number
        self.db.do('users', {'id': self.id, 'phone': int(phone)}, condition=f"id={self.id}")
        self.user_info=self.get_user_info_from_db([])
        self.send_message('phone_shared', self.menu_keys)
        return -1
    e.callback = act
    p.entry=[e1,e]
    return p
            
def SelectLanguagePack(self:Conversation,**kargs):
    get_text_setting =kargs.get('get_text_setting',False)
    # next_check= kargs.get('next_check')
    p = Pack()
    p.name = 'select_language'
    e=Node()
    e.filters =SelectLanguageFilter(self)
    def act(self:Conversation,*a):
        btn = {k:f"{v}:select_language" for k,v in self.languages.items()}
        self.send(msg='Select_your_Language', btns= btn,get_text_setting=get_text_setting,close=False)
        return -1
    e.callback =act

    e2=Node()
    e2.command ='Language'
    def act(self:Conversation,*a):
        btn = {k:f"{v}:select_language" for k,v in self.languages.items()}
        self.send(msg='Select_your_Language', btns= btn,get_text_setting=get_text_setting,close=False)
        # if type(next_check)!=type(None):
        #     next_check(self)
        return -1
    e2.callback =act

    e1 = Node()
    e1.pattern = self.check_inline_keyboards('select_language',1)
    def act(self:Conversation,*args):
        lang_id = int(self.splited_query_data()[1])
        self.db.do('users', {'id': self.id, 'language': lang_id}, condition=f"id={self.id}")
        self.delete_message(self.get_msg_id())
        self.user_info=self.get_user_info_from_db([])
        self.send('language_set', self.menu_keys,get_text_setting=get_text_setting)
        
        return -1
    e1.callback = act
    p.entry=[e,e1,e2]
    return p
            
def Referral(self:Conversation):
    p = Pack()
    p.name = 'Referral'
    p.db_config={'users':{'presenter':0}}

    e1 = Node()
    e1.btn = self.menu_keys
    e1.filters = match_btn('referral',self)
    
    def referral_text(self:Base,*args):
        msg=self.text('referral_text',slash=True)+'\n\n'
        msg+=f'https://t.me/{self.super_self.bot_username}?start=ref{self.id}\n\n'
        msg+=f"{self.text('invited')} : {len(self.db.do('users', condition=f'presenter={self.id}'))}"

        self.send(msg= msg,btns=self.menu_keys,translat=False)
        return -1
    e1.callback =referral_text

    e2 = Node()
    e2.btn = self.menu_keys
    e2.command = 'start'
    e2.command_filters=Filters.regex('/start ref\d+')
    def referral_action(self,*args):
        try:
            presenter = int(self.get_text().split(' ')[-1].replace('ref',''))
        except:
            try:
                presenter = int(self.splited_query_data()[1].split(' ')[-1].replace('ref',''))
            except:
                presenter=0
        try:
            submited_presenter = int(self.user('presenter'))
        except:
            submited_presenter = 0
        if submited_presenter==0 and presenter!=self.id:
            self.db.do('users', {'presenter': presenter},condition=f"id={self.id}")
            self.send('new_subset_text', chat_id=presenter)
        self.send('start_pm', self.menu_keys)
        return -1
    
    e2.callback=referral_action

    e3 = Node()
    e3.btn = self.menu_keys
    e3.pattern = self.check_inline_keyboards('/start ref',2,regex=True)
    e3.callback=referral_action


    p.entry=[e1,e2,e3]
    return p
def ToggleSetting(self:Conversation,**kargs):
    p=Pack()
    key = kargs.get('key','toggle_setting')
    p.name = key
    def setting_msg_btn(self):
        setting = self.db.do('setting',condition=f"subset='{key}'")
        msg=''
        btn={}
        for i in setting:
            msg+=f"{self.text(i['key'],slash=True)} : {self.text(i['value'])}\n"
            btn[i['key']]=key
        return msg,btn

    e=Node()
    e.filters = match_btn(key,self)
    def act(self:Conversation,*args):
        msg,btn = setting_msg_btn(self)
        self.send(msg,btn,translat=False)
        return self.stat_key(key,0)
    e.callback=act

    s=Node()
    s.pattern = self.check_inline_keyboards(key,1)
    def act(self:Conversation,*args):
        k = self.splited_query_data()[0]
        res = self.toggle('setting','value',k,'key',['0','1'])
        self.alert(self.text(res))
        msg,btn = setting_msg_btn(self)
        self.edit_message_text(msg,self.get_msg_id(),btn,t=False)
        return self.stat_key(key,0)
    s.callback=act

    p.entry=[e]
    p.states=[[s]]

    return p

def Status(self:Conversation,**kargs):
    p=Pack()
    subset = kargs.get('key','toggle_setting')
    column = kargs.get('column','subset')

    msg = kargs.get('msg','click_option')
    table = kargs.get('table','setting')
    value = kargs.get('value','value')
    key = kargs.get('target','key')
    p.name = subset
    def setting_msg_btn(self):
        setting = self.db.do('setting',condition=f"{column}='{subset}'")
        btn=[]
        for item in setting:
            sbtn=[
                telegram.InlineKeyboardButton(self.text(item[key]),callback_data=f'{item[key]}:{subset}slbl'),
                telegram.InlineKeyboardButton(self.text(item[value]),callback_data=f'{item[key]}:{subset}set_stat'),
            ]
            btn+=[sbtn]
        btn = telegram.InlineKeyboardMarkup(btn)
        return msg,btn
    e=Node()
    e.filters = match_btn(subset,self)
    def act(self:Conversation,*args):
        msg,btn = setting_msg_btn(self)
        self.send(msg,btn)
        return -1
    e.callback=act
    ###############################
    s=Node()
    s.pattern =self.check_inline_keyboards(subset+'slbl',1)
    def act(self:Conversation,*a):
        name = self.splited_query_data()[0]
        self.alert(self.text(name))
        return -1
    s.callback=act
    ###############################
    s1=Node()
    s1.pattern =self.check_inline_keyboards(subset+'set_stat',1)
    def act(self:Conversation,*a):
        name = self.splited_query_data()[0]
        res = self.toggle(table,value,name,cond_col=key,switch=['0','1'])
        _,btn = setting_msg_btn(self)
        self.edit_message_reply_markup(btn,self.get_msg_id(),col=4)
        return -1
    s1.callback=act
    p.entry=[e,s,s1]
    return p

def Setting(self:Conversation,**kargs):
    p=Pack()
    key = kargs.get('key','public_setting')
    p.name = key
    slash = kargs.get('slash',True)
    def setting_msg_btn(self):
        setting = self.db.do('setting',condition=f"subset='{key}'")
        msg=''
        btn=[]
        for i in setting:
            if i.get('hide')!=1:
                msg+=f"{self.text(i['key'],slash=slash)} : \n{i['value']} {self.text(i['unit'],slash=True)}\n---\n"
            btn+=[i['key']]
        if msg=='':msg=self.text('select_option',slash=True)
        return msg,btn

    e=Node()
    e.filters = match_btn(key,self)
    def act(self:Conversation,*args):
        msg,btn = setting_msg_btn(self)
        self.send(msg,chunks(btn,2)+[[self.back_menu_key]],translat=False)
        return self.stat_key(key,0)
    e.callback=act

    s=Node()
    s.filters = Filters.text
    def act(self:Conversation,*args):
        msg,btn = setting_msg_btn(self)
        k = self.get_btn_key_as_text(self.get_text())
        if k in btn:
            msg='enter_new_value'
            self.userdata('set_key',k)
            self.send(msg,[[self.back_menu_key]])
            return self.stat_key(key,1)
        else:
            btn+=[self.back_menu_key]
            self.send(msg,chunks(btn,2),col=2,translat=False)
            return self.stat_key(key,0)
    s.callback=act


    s1=Node()
    s1.filters = Filters.text
    def act(self:Conversation,*args):
        k = self.userdata('set_key')
        if self.set_setting(k,self.get_text()):
            self.send('updated')
        else:
            self.send(self.text('bad_input',slash=True)+'\n'+self.text('enter_new_value',slash=True))
            return self.stat_key(key,1)

        msg,btn = setting_msg_btn(self)
        self.send(msg,chunks(btn,2)+[[self.back_menu_key]],col=2,translat=False)
        return self.stat_key(key,0)
    s1.callback=act

    p.entry=[e]
    p.states=[[s],[s1]]

    return p
    
def SettingPro(self:Conversation,**kargs):
    p=Pack()
    key = kargs.get('key','setting_pro')
    p.name = key
    slash = kargs.get('slash',True)
    def setting_msg_btn(self):
        setting = self.db.do('setting',condition=f"subset='{key}'")
        msg=''
        btn=[]
        toggle_btn=[]
        toggle_msg='click_option'
        for i in setting:
            if i.get('hide')!=1:
                if i.get('toggle')==1:
                    sbtn=[                        
                        telegram.InlineKeyboardButton(self.text(i['key']),callback_data=f"{i['key']}:{key}slbl"),
                        telegram.InlineKeyboardButton(self.text(i['value']),callback_data=f"{i['key']}:{key}set_stat"),
                    ]
                    toggle_btn+=[sbtn]
                else:
                    msg+=f"{self.text(i['key'],slash=slash)} : \n{i['value']} {self.text(i['unit'],slash=True)}\n---\n"
                    btn+=[i['key']]
            
        if msg=='':msg=self.text('select_option',slash=True)
        if toggle_btn:
            toggle_btn = telegram.InlineKeyboardMarkup(toggle_btn)

        return msg,btn,toggle_msg,toggle_btn

    e=Node()
    e.filters = match_btn(key,self)
    def act(self:Conversation,*args):
        msg,btn,toggle_msg,toggle_btn = setting_msg_btn(self)
        if toggle_btn:
            self.send(toggle_msg,toggle_btn,translat=False)
        if btn:
            self.send(msg,chunks(btn,2)+[[self.back_menu_key]],translat=False)
        return self.stat_key(key,0)
    e.callback=act

    ###############################
    ss=Node()
    ss.pattern =self.check_inline_keyboards(key+'slbl',1)
    def act1(self:Conversation,*a):
        name = self.splited_query_data()[0]
        self.alert(self.text(name))
        return self.stat_key(key,0)
    ss.callback=act1
    ###############################
    ss1=Node()
    ss1.pattern =self.check_inline_keyboards(key+'set_stat',1)
    def act2(self:Conversation,*a):
        name = self.splited_query_data()[0]
        res = self.toggle('setting','value',name,cond_col='key',switch=['0','1'])
        _,_,_,toggle_btn = setting_msg_btn(self)
        self.edit_message_reply_markup(toggle_btn,self.get_msg_id(),col=4)
        return self.stat_key(key,0)
    ss1.callback=act2


    s=Node()
    s.filters = Filters.text
    def act(self:Conversation,*args):
        msg,btn,_,_ = setting_msg_btn(self)
        k = self.get_btn_key_as_text(self.get_text())
        if k in btn:
            msg='enter_new_value'
            self.userdata('set_key',k)
            self.send(msg,[[self.back_menu_key]])
            return self.stat_key(key,1)
        else:
            self.send(msg,chunks(btn,2)+[[self.back_menu_key]],col=2,translat=False)
            return self.stat_key(key,0)
    s.callback=act


    s1=Node()
    s1.filters = Filters.text
    def act(self:Conversation,*args):
        k = self.userdata('set_key')
        if self.set_setting(k,self.get_text()):
            self.send('updated')
        else:
            self.send(self.text('bad_input',slash=True)+'\n'+self.text('enter_new_value',slash=True))
            return self.stat_key(key,1)

        msg,btn,_,_ = setting_msg_btn(self)
        self.send(msg,chunks(btn,2)+[[self.back_menu_key]],col=2,translat=False)
        return self.stat_key(key,0)
    s1.callback=act

    p.entry=[e]
    p.states=[[s,ss,ss1],[s1]]

    return p
   
def Products(self:Conversation,**kargs):
    p=Pack()
    row = kargs.get('row',5)
    p.name='products'
    p.db_config = {
        'products':{
            'id':0,
            'title':'',
            'price':0.,
            'status':0,
            'time':0,
        }
        }
    e = Node()
    e.filters = match_btn('products', self)
    def act(self:Conversation,*args):
        products = self.db.do('products')
        main_btn = [['add_product'],[self.back_menu_key]]
        if products:
            self.send('products_list',btns=main_btn)
            msg =[]
            for i in products:
                msg+=[f"{i['title']}\n/p_{i['id']}\n\n"]
            msg,btn = self.pagination_maker(msg,row)
            self.send(msg=msg,btns=btn,t=False)

        else:
            self.send('no_item',main_btn)
        return -1
    e.callback = act
    p.entry=[e]
    return p

def Orders(self:Conversation,**kargs):
    p=Pack()
    row = kargs.get('row',5)
    p.name='orders'
    p.db_config = {
        'orders':{
            'id':0,
            'pid':'',
            'uid':'',
            'price':0.,
            'status':0,
            'time':0,
        }
        }
    e = Node()
    e.filters = match_btn('orders', self)
    def act(self:Conversation,*args):
        orders = self.db.do('orders')
        main_btn = self.menu_keys
        if orders:
            self.send(msg,btns=main_btn,translat=False)
            msg =[]
            for i in orders:
                msg+=[f"/o_{i['id']}\n"]
            msg,btn = self.pagination_maker(msg,row)
            self.send(msg=msg,btns=btn,t=False)
        else:
            self.send('no_item',main_btn)
        return -1
    e.callback = act
    p.entry=[e]
    return p

from .filteres import match_btn
from .enum import *

def Multi(self:Conversation,name,items:list,check_sign='✅',table='setting',cond='key=',target='value',target_type=str,close=True):
    items = dict(zip(range(len(items)),items))
    p =Pack()
    p.name = name
    e=Node()
    e.filters = match_btn(name,self)
    def act(self:Conversation,*a):
        msg= f'{name}_txt'
        value = int(str(self.db.do(table,condition=cond)[0][target]))
        if value==None:value=0
        btn = {}
        for k,v in items.items():
            sign=''
            if value==k:
                sign = check_sign+' '
            btn[sign+self.text(v)] = f"{k}:multi_{name}"
        self.send(msg,btn,close=close,col=1)
        return -1
    e.callback=act
    # self.node('name',[e])
    #############################
    e1=Node()
    e1.pattern = self.check_inline_keyboards(f'multi_{name}',1)
    def act(self:Conversation,*a):
        tid = int(self.splited_query_data()[1])
        value = int(str(self.db.do(table,condition=cond)[0][target]))


        if tid== value:return -1
        
        try:ctid=target_type(tid)
        except:ctid=tid
        self.db.do(table,{target:ctid},condition=cond)
        self.user_info = self.get_user_info_from_db([])
        value = int(str(self.db.do(table,condition=cond)[0][target]))
        if value==None:value=0
        btn = {}
        for k,v in items.items():
            sign=''
            if value==k:
                sign = '✅ '
            btn[sign+self.text(v)] =  f"{k}:multi_{name}"
        self.edit_message_reply_markup(btn,self.get_msg_id(),col=1,close=close)
        return -1
    e1.callback=act
    p.entry=[e,e1]
    return p
    # self.node(f'sub{name}',[e])


from ..classes import Conversation
import time
# from .functions import translator
from starco.utils import translator

##############################3
def translate(self:Conversation):
    
    e= Node()
    e.filters = match_btn('translate',self)
    def act(self:Conversation,*a):
        btn ={k:f'{v}:src_lang' for k,v in self.languages.items()}
        self.send('select_from',btn)
        return self.stat_key('translate',0)
    e.callback =act

    s=Node()
    s.pattern = self.check_inline_keyboards('src_lang',1)
    def act(self:Conversation,*a):
        print(2)
        self.userdata('src_lang',int(self.splited_query_data()[1]))
        btn ={k:f'{v}:trgt_lang' for k,v in self.languages.items()}
        self.edit_message_text('select_target',self.get_msg_id(),btn)
        return self.stat_key('translate',1)
    s.callback=act

    s1=Node()
    s1.pattern = self.check_inline_keyboards('trgt_lang',1)
    def act(self:Conversation,*a):
        self.delete_message(self.get_msg_id())
        self.wait()
        trgt_lang = int(self.splited_query_data()[1])
        src_lang = self.userdata('src_lang')
        texts = self.db.do('texts',condition=f"role={self.role} AND language={src_lang}")
        ex_texts = [i['key'] for i in self.db.do('texts',condition=f"role={self.role} AND language={trgt_lang}")]
        texts =[i for i in texts if i['key'] not in ex_texts]
        out=[]
        langs_pfx = {v:k for k,v in self.languages.items()}
        target = langs_pfx[trgt_lang]
        for i in texts:
            value = i['value']
            #do translat
            value = translator(value,target)
            if value==None:continue
            i['value']=value
            i['language'] = trgt_lang
            i['role'] = self.role
            i['id']=self.time()
            out+=[i.copy()]
            time.sleep(0.01)
        self.db.do('texts',out)
        self.send('done')
        return -1
    s1.callback=act
    self.node('translate',[e],[[s],[s1]])


from threading import Thread
from functools import partial


def SendToAllBasic(self:Conversation):
    p=Pack()
    p.name = 'send_to_all_basic'

    e = Node()
    e.filters = match_btn('send_to_all', self)
    e.msg = 'enter_your_message'
    e.btn = [[self.back_menu_key]]

    s = Node()
    s.filters = Filters.all
    def act(self: Conversation, *args):
        msg_id, chat_id = self.get_msg_id(), self.get_chat_id()
        Thread(target=partial(self.send_to_users, msg_id, chat_id,None,[self.id])).start()
        self.send_message('message_is_sending', self.menu_keys)
        return -1
    s.callback = act

    p.entry=[e]
    p.states=[[s]]
    return p

#************** not completed********************
def SupportAdmin(self:Conversation):
    p = Pack()
    p.name = 'SupportAdmin'
    p.db_config={'support': {'id':0,'u_id': 0, 'msg_id': 0, 'response_id': 0, 'responser_id': 0, 'extra': '', 'status': 0, 'time': 0}}
    e=Node()
    e.filters = match_btn('support',self)

    def show_message_from_user(self:Conversation, item):
        try:

            lnk = None
            u_username = self.user('username')
            if u_username != None:
                lnk = f'https://t.me/{u_username}'
            try:
                name = self.user('name')[:13]
            except:
                name = 'info'
            btn = {
                'send_reply': f"{item['id']}",
                'user_info': f"{item['u_id']}",
                'mark_read': f"{item['id']}",
                'show_response': f"{item['id']}",
                'perv_sup_pm': f"{item['id']}:{item['u_id']}",
                'next_sup_pm': f"{item['id']}:{item['u_id']}",
            }
            tbtn = btn.copy()
            tbtn[name] = f"shinfo:{item['id']}"
            if lnk:
                tbtn['pv'] = lnk
            
            try:
                self.copy_message(from_chat_id=item['u_id'],message_id=item['msg_id'],chat_id=self.id,btns=tbtn)
            except:
                try:
                    btn['info'] = f"shinfo:{item['time']}"
                    if lnk:
                        btn['pv'] = lnk
                        self.copy_message(from_chat_id=item['u_id'],message_id=item['msg_id'],chat_id=self.id,btns=tbtn)
                except:
                    self.send('unreadable_message'+f"\n/user_{item['u_id']}", btn)
                    self.db.do('support', {'status': 1},condition=f"id={item['id']}")
        except Exception as e:
            self.send_message('unreadable_message'+f"\n/user_{item['u_id']}\nerror")
            self.db.do('support', {'status': 1},condition=f"id={item['id']}")
            self.log(e)


    def unreaded_messages(self:Conversation, *args):
        unreaded_messages = self.db.do('support', condition=f"status=0")
        self.send('wait', self.menu_btn)
        try:
            if not unreaded_messages:
                self.send('no_item', self.menu_keys)
            else:
                for item in unreaded_messages:
                    self.show_message_from_user(item)
        except Exception as e:
            self.log(e)
        return -1
    e.callback = unreaded_messages
    p.entry=[e]
    return p


    
    
