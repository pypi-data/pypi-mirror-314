from starco.utils import *
import os,shutil
from starco.tlg.app.utils import get_number
from .enum import *
from .filteres import *
from ..classes import Conversation
from telegram.ext import Filters
import time
from starco.tlg.app import TlgApp
def setuper(value:str,subset:str,unit:str='',type:str='',hide:int=0,toggle:int=0):
    return {'value':value,'subset':subset,'unit':unit,'type':type,'hide':hide,'toggle':toggle}

def SpamBot_req(number):
    tlg = TlgApp(number)
    time.sleep(1)
    status,_=tlg.get_account_status()
    if status!='ban':
        tlg.disconnect()
        return
    time.sleep(2)
    tlg.get_telegram_code
    tlg.send_message('SpamBot','Submit a complaint')
    time.sleep(2)
    tlg.send_message('SpamBot','No, I’ll never do any of this!')
    time.sleep(7)
    pm='Dear Telegram Support!\nMy Telegram Account has been spammed suddenly and I cannot sent message to any contacts whom I don’t have their number and I want you to help me and fix the issue and remove my number from blacklist.'
    tlg.send_message('SpamBot',pm)
    tlg.disconnect()

def backup_database(self,chat_id=''):
    try:
        path = self.db.path
        database_dir = path_maker(['database'])
        shutil.copy2(path,database_dir)
        zip_path = path_maker([],'.')+'/database.zip'
        zipfolder(zip_path,database_dir)
        print(zip_path)
        with open(zip_path,'rb') as f:
            if chat_id=='':chat_id = self.host_id
            print(chat_id)
            self.bot.bot.send_document(chat_id, f,caption=self.get_bot_username())
    finally:
        try:os.remove(zip_path)
        except:pass
        try:shutil.rmtree(database_dir)
        except:pass

def copy_ready_session(zip_path,saved_before):
    rootdir=path_maker(['zipdir'],'.')
    unziper(zip_path,rootdir)
    sessions={}
    for root, subdirs, files in os.walk(rootdir):
        for filename in files:
            number = get_number(filename)
            if number in saved_before:
                print('duplicated')
                continue
            if number and number>0:
                file_path = os.path.join(root, filename)
                sessions[number]=sessions.get(number,{})
                if filename.endswith('.session'):
                    sessions[number]['session']=file_path
                elif filename.endswith('.json'):
                    sessions[number]['json']=file_path
    ow_path=lambda number,x:os.path.join(path_maker(['accounts',number],'.'),f"+{(x.split('/')[-1]).lstrip('+')}")
    print(sessions)
    for number , values in sessions.items():
        if 'session' not in values or 'json' not in values:continue
        print(values['session'],ow_path(number,values['session']))
        print(values['json'],ow_path(number,values['json']))
        shutil.move(values['session'],ow_path(number,values['session']))
        shutil.move(values['json'],ow_path(number,values['json']))

    shutil.rmtree(rootdir)
    os.remove(zip_path)
    return list(sessions.keys())

def get_product(self,id:int,status=CONFIRMED):
    try:
        return self.db.do('products',condition=f"id={id} AND status={status}")[0]
    except:return {}

def get_orders_by_pid(self,pid:int,status=WAITING):
    try:
        return self.db.do('orders',condition=f"pid={pid} AND status={status}")
    except:return []

def get_order(self,id:int,status=WAITING):
    try:
        return self.db.do('orders',condition=f"id={id} AND status={status}")[0]
    except:return {}

def setup_force_join(self):
    e = Node()
    e.filters = match_btn('force_join', self)

    def act(self: Conversation, *args):
        force_joins = self.db.do('force_join')
        if force_joins:
            self.send('lists', [['add_force_join'], [self.back_menu_key]])

            for i in force_joins:
                msg = f"{self.text('title',slash=True)}: {i['title']}\n"
                msg += f"{self.text('channel_id',slash=True)}: {i['channel_id']}"
                msg += f"{self.text('link',slash=True)}: {i['link']}"
                self.send(msg, {'delete_fj': i['id']}, t=False)
        else:
            self.send('no_item', [['add_force_join'], [self.back_menu_key]])
        return -1
    e.callback = act
    self.node('force_join', [e])
    ########################################
    e = Node()
    e.pattern = self.check_inline_keyboards('delete_fj')

    def act(self: Conversation, *args):
        id = int(self.splited_query_data()[1])
        self.db.do('force_join', delete=True)
        self.edit_message_text('deleted', self.get_msg_id())
        return -1
    e.callback = act
    self.node('delete_fj', [e])
    ########################################
    e = Node()
    e.filters = match_btn('add_force_join', self)
    e.msg = 'enter_title'
    e.btn = [[self.back_menu_key]]

    s = Node()
    s.filters = Filters.text
    s.msg = 'enter_channel_id'
    s.btn = [[self.back_menu_key]]

    s1 = Node()
    s1.filters = Filters.text
    s1.msg = 'enter_channel_link'
    s1.btn = [[self.back_menu_key]]

    s2 = Node()
    s2.filters = Filters.text
    def act(self: Conversation, *args):
        title = self.userdata(self.stat_key('add_force_join', 1))['text']
        channel_id = self.userdata(self.stat_key('add_force_join', 2))['text']
        link = self.get_text()
        self.db.do('force_join', {'id': self.time(), 'title': title,'channel_id':channel_id, 'link': link,'status':CONFIRMED})
        self.send('done', self.menu_keys)
        return -1

    s2.callback = act
    self.node('add_force_join', [e], [[s],[s1], [s2]])
 