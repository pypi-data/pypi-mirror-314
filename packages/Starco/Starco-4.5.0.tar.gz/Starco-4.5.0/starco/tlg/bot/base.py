import requests,json
from starco.debug import Debug
from starco.utils import get_timestamp ,chunks
from time import sleep
from .util.enum import BTN_PFX, Role, HeadPack
from starco.db import DB
from functools import wraps
import copy
from telegram.ext import MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from .util.enum import ConversationNode, Node, Pack
from .util.filteres import IsReplied, match_btn, RoleFilter
from time import sleep
import telegram
from telegram.ext import Filters
from .util.filteres import match_btn
import types,json
from telegram import Update,MessageEntity,Bot,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton

 
class Base:
    def __init__(self, super_self, *args, **kwargs) -> None:
        self.type = self.__class__.__name__
        self.super_self = super_self
        self.defulat_lang_code=kwargs.get('defulat_lang_code',0)
        self.languages=kwargs.get('languages',{})
        self.host_channel_id = super_self.host_id
        self.superAdmins = self.super_self.superAdmins
        self.update:Update = None
        self.context = None
        self.role = kwargs.get('role')
        self.user_info = None
        self.id = 0
        self.msg_id = 0
        self.back_key = 'back'
        self.back_menu_key = 'menu'
        self.menu_keys = []
        self.lang_code=-1
        self.text_list=[]
        self.log: Debug = super_self.log
        if type(self.log) == type(None):
            raise Exception('Debug Class Not defined')

        self.db: DB = super_self.db

        self.bot: Bot = super_self
        if type(self.bot) == type(None):
            raise Exception('bot Not defined')

        self.status = False
        self.checkpoints = {}

        self.go_menu_filter = match_btn(self.back_menu_key, self)
        self.go_back_filter = match_btn(self.back_key, self)

    def tail(self, func_name, *args, **kargs):
        if self.status:
            last_checkpoint = self.userdata('checkpoint')
            self.userdata('checkpoint', delete=True)
            if last_checkpoint:
                self.user_info = self.get_user_info_from_db([])
                self.run_checkpoint('NotNull')

    def head(self, func_name, *args, **kargs):
        print(func_name)
        if args:
            for i in args:
                if (i.__class__.__name__ == 'Update'):
                    self.update = i
                elif (i.__class__.__name__ == 'CallbackContext'):
                    self.context = i
                    
            try:
                if not self.update:
                    return
            except:
                return
            self.id = self.get_id()
            self.update_user()
            self.user_info = self.get_user_info_from_db([])
            if self.user('role') !=self.role or (self.user('status')!=1 and not self.is_super_admin()):
                self.status=False
                return
            if (self.user('role')!= Role.ADMIN.value and not self.is_super_admin()) and self.get_setting('bot_status')!=1:
                self.send('bot_off_text',get_text_setting=True)
                self.status=False
                return
            forbid_list = ['setter', 'menu_btns']
            print(func_name)
            for i in forbid_list:
                if i in func_name:break
            else:
                print(f"{func_name} set")
                self.userdata('last_function_name', func_name)
            self.status = self.run_checkpoint(func_name)

    def run_checkpoint(self, func_name):
        for key, func in self.checkpoints.items():
            res = func(self)
            go_on = True
            if not isinstance(res, bool):
                res, go_on = res
            if not go_on:
                self.userdata('checkpoint', key)
                return False

            

            if res in [False, None] :
                self.userdata('checkpoint', key)
                return False

            

        return True

    def detect_type(self, item: Node):
        if item.filters:
            return MessageHandler
        elif item.command:
            return CommandHandler
        elif item.pattern:
            return CallbackQueryHandler
        raise Exception(
            f"{self.element_name} havent true input for detect type")

    def dict_from_node(self, item: Node, idx: int, name: str, states_count: int = 0, level=-1):
        if not item.callback:
            def callback(self: Base, *args):
                id = self.stat_key(name,level)
                self.userdata(id,
                              {
                                  'text': self.get_text(),
                                  'query': self.splited_query_data(),
                                  'msg_id': self.get_msg_id(),
                              })
                msg = id
                if item.msg:
                    msg = item.msg
                btn = item.btn
                self.send(msg=msg, btns=btn,
                          chat_id=item.chat_id, **item.send_args)
                rtn_idx = -1
                if item.state_idx:
                    rtn_idx = item.state_idx

                elif level == (states_count) or level == -1:
                    rtn_idx = -1
                else:
                    rtn_idx = self.stat_key(name,level)
                return rtn_idx
            callback.__name__ = name+f"_{idx}_{level}"
            item.callback = self.add_method(callback, name+f"_{idx}")
        else:
            item.callback = self.add_method(item.callback,name+f"_{idx}")
        out = {'callback': item.callback}
        if item.filters:
            out['filters'] =  item.filters & RoleFilter(self)
            if level!=0:
                out['filters'] = ~self.go_menu_filter & out['filters']
        elif item.command:
            out['command'] = item.command
            
            out['filters'] = RoleFilter(self)
            if level!=0:
                out['filters'] = ~self.go_menu_filter & out['filters']
            if item.command_filters:
                out['filters'] = out['filters'] & item.command_filters

        elif item.pattern:
            if isinstance(item.pattern, str):
                item.pattern = self.check_inline_keyboards(item.pattern)
            out['pattern'] = item.pattern
            out['pass_user_data'] = True
            

        return out

    def menu(self,*args):
        self.send('menu_text',self.menu_keys)
        return -1
    
    def stat_key(self,name,level):
        out =  f"{name}_{level}_{str(self.role)}"
        return out
    
    def add_method(self, func, name=''):
        if name == '':
            name = 'mf_' + str(self.role) + f"_{str(func.__name__)}"
        self.__dict__[name] = types.MethodType(self.action_on_call(func,name), self)
        return self.__dict__[name]

    def node(self, name: str, entry: list[Node], states: list[Node] = None, fallbacks: list[Node] = None, db_config: dict[dict] = {}, **kargs):
        self.element_name = name
        if db_config:
            for k,v in db_config.items():
                self.super_self.add_table(k,v)
            self.super_self.init_db()
            
        conversation = ConversationNode()
        states_count = 0 if not states else len(states)
        level = 0
        for i, item in enumerate(entry):
            handler = self.detect_type(item)(
                **self.dict_from_node(item, idx=i, name=name, states_count=states_count, level=level))
            conversation.entries += [handler]
            level += 1
        # conversation.entries=[CommandHandler('start',self.start)]
        if states:
            for i, state in enumerate(states):
                if not isinstance(state, list):
                    state = [state]
                result = []
                for item in state:
                    handler = self.detect_type(item)(
                        **self.dict_from_node(item, idx=i, name=name, states_count=states_count, level=level))
                    result += [handler]
                idx= self.stat_key(name,level-1)
                conversation.states[idx] = result
                level += 1
        if fallbacks:
            for i, item in enumerate(fallbacks):
                conversation.fallbacks += [self.detect_type(item)(
                    **self.dict_from_node(item, idx=i, name=name))]
        else:
            conversation.fallbacks = [MessageHandler(
                match_btn(self.back_menu_key, self), self.add_method(self.menu))]
        conversation.arges = {**kargs}
        self.nodes += [conversation]

    def pack(self, pack, repalce_callback_func_name: str = None,**pack_kargs):
        if pack_kargs:
            pack: Pack = pack(self,**pack_kargs)
        else:pack: Pack = pack(self)
        if repalce_callback_func_name:
            for entry in pack.entry:
                try:
                    entry.callback.__name__ = repalce_callback_func_name
                except Exception as e:
                    self.log(e)

        self.node(
            name=pack.name,
            entry=pack.entry,
            states=pack.states,
            fallbacks=pack.fallbacks,
            db_config=pack.db_config,
            **pack.kargs
        )
        return pack

    def action_on_call(self, func,name):
        @wraps(func)
        def wrapper(self, *args, **kw):
            self.head(name, *args, **kw)
            res = None
            try:
                try:
                    status = self.status
                except:
                    status = False
                if status:
                    try:
                        res = func(self, *args, **kw)
                    except Exception as e:
                        self.log(e)
            finally:
                pass
            self.tail(func.__name__, *args, **kw)

            return res
        return wrapper

    def add_head(self, head_pack: HeadPack):
        '''
            func(self)
        '''
        head_pack = head_pack(self)
        if head_pack.db_config:
            self.super_self.db_config = {
                **self.super_self.db_config, **head_pack.db_config}
        if head_pack.pack:
            self.pack(head_pack.pack, repalce_callback_func_name=head_pack.name)

        self.checkpoints[head_pack.name] = head_pack.func

    #################################################
    def time(self):
        return get_timestamp('now')

    def is_super_admin(self):
        if self.id in self.superAdmins:
            return True
        return False

    def get_id(self):
        if 'callback_query' in self.update.to_dict():
            return self.update.callback_query.message.chat.id
        else:
            return self.update.message.from_user.id

    def get_name(self):
        if 'callback_query' in self.update.to_dict():
            return self.update.callback_query.message.chat.first_name
        else:
            return self.update.message.from_user.first_name

    def get_username(self):
        try:
            if 'callback_query' in self.update.to_dict():
                return self.update.callback_query.message.chat.username
            else:
                return self.update.message.from_user.username
        except:
            pass
        return None

    def get_last_name(self):
        if 'callback_query' in self.update.to_dict():
            return self.update.callback_query.message.chat.last_name
        else:
            return self.update.message.from_user.last_name

    def get_reply_markup(self, per_row_item=3,**kargs):
        reply_markup = self.update.callback_query.message.reply_markup.inline_keyboard
        res = {}
        for i in reply_markup:
            for btn in i:
                if 'callback_data' in btn.to_dict():
                    item = str(btn.callback_data)
                    sitem = item.split(':')
                    res[sitem[0]] = ":".join(sitem[1:])
                else:
                    res[btn.text] = str(btn.url)
        return self.inline_keyboard_maker(res, col=per_row_item,**kargs)

    def get_msg_id(self):
        if 'callback_query' in self.update.to_dict():
            return self.update.callback_query.message.message_id
        else:
            return self.update.message.message_id

    def get_chat_type(self):
        try:
            if 'callback_query' in self.update.to_dict():
                return self.update.callback_query.message.chat.type
            else:
                return self.update.message.chat.type
        except:
            pass

    def get_chat_id(self):
        if 'callback_query' in self.update.to_dict():
            return self.update.callback_query.message.chat.id
        else:
            return self.update.message.chat.id

    def get_type(self):
        try:
            if 'callback_query' in self.update.to_dict():
                return self.update.callback_query.message.chat.type
            else:
                return self.update.message.chat.type
        except:
            pass
    
    def get_msg_entities(self):
        return json.dumps([i.to_dict() for i in self.update.effective_message.entities])

    def msg_entities_json_entities_class(self,json_msg_entities):
        return [MessageEntity(**i) for i in json.loads(json_msg_entities)]

    def get_text(self, callback_deny=False):
        try:
            if not callback_deny and 'callback_query' in self.update.to_dict():
                return self.update.callback_query.message.text
        except:
            pass
        try:
            return self.update.message.text
        except:
            pass
    
    def get_btn_key_as_text(self,txt):
        k,_ = self.text(txt, True, 'value',slash=False)
        return k.replace(BTN_PFX, '')

    def splited_query_data(self, splitor=':'):
        try:
            data = self.update.callback_query.data
            return data.split(splitor)
        except:
            pass

    ###################################################
    def toggle(self, table: str, column: str, id, cond_col='id', switch=[0, 1]):
        if isinstance(id,str):
            cond= f"{cond_col}='{id}'"
        else:cond= f"{cond_col}={id}"
        res = self.db.do(table, condition=cond)
        if res:
            new_val = switch[-1]
            if res[0].get(column) == switch[-1]:
                new_val = switch[0]
            self.db.do(table, {column: new_val},cond)
            return new_val

    def userdata(self, key, value=None, delete=False, regex=False):
        if delete:
            try:
                self.context.user_data.pop(key)
            except:
                pass
            return
        if type(value) == type(None):
            if regex:
                out = {}
                for k, v in self.context.user_data.items():
                    if key in k:
                        out[k] = v
                return out
            return self.context.user_data.get(key)
        else:
            # if value != self.get_btn_value(self.back):
            self.context.user_data[key] = value
    ###################################################

    ###################################################
    def get_setting(self, key, return_row=False):
        try:
            row = self.db.do('setting', condition=f"key='{key}'")
            row = row[0]
            if return_row:
                return row
            if row['type'] == '':
                return row['value']
            else:
                try:
                    # if row['type'] == 'Language':

                    #     return Language.get_value_by_name(row['value'])
                    return eval(row['type'])(row['value'])
                except Exception as e:
                    self.log(e)
                    return None
        except:
            return None

    def set_setting(self, key, value):
        try:
            row = self.db.do('setting', condition=f"key='{key}'")
            if row:
                row = row[0]
                if row['type'] != '':
                    try:
                        value = eval(row['type'])(value)
                    except Exception as e:
                        self.log(e)
                        return False
            self.db.do(
                'setting', {'key': key, 'value': value}, condition=f"key='{key}'")
            return True
        except Exception as e:
                self.log(e)
        return False

    def user(self, key):
        try:
            return self.user_info[key]
        except:
            data = self.get_user_info_from_db([])
            if isinstance(data, list):
                self.user_info = data[0]
                return self.user_info.get(key)
                
            elif isinstance(data, dict):
                self.user_info = data
                return self.user_info.get(key)

    def update_user(self):
        try:
            data = {
                'id': self.id,
                'name': self.get_name(),
                'last_name': self.get_last_name(),
                'username': self.get_username(),
                'is_online': 1,
                'last_seen': self.time()
            }
            if self.is_super_admin():
                data['role'] =  Role.ADMIN.value
            user = self.db.do('users', condition=f"id={self.id}")
            try:
                user = user[0]
            except:
                user = {}

            if user.get('time') in [0, None]:
                first_cfg = {
                    'editor': 0,
                    'status': 1,
                    'get_alarm': 1,
                    'phone': 0,
                    'language': self.defulat_lang_code,
                }
                data = {**data, **first_cfg}
                data['time'] = self.time()
                role = Role.USER.value
                if self.is_super_admin():
                    role = Role.ADMIN.value
                data['role'] = role
            self.db.do('users', data, condition=f"id={self.id}")

        except Exception as e:
            self.log(e)

    def get_user_info_from_db(self, key_s, id=0):
        '''
        if str : return str
        elif list and empty return all info as dict
        else return requested info in list as dict
        '''
        if id == 0:
            id = self.id
        try:
            if isinstance(key_s, list):
                if id==0:return {}
                if key_s:
                    return {k: v for k, v in self.db.do('users', condition=f"id={id}")[0].items() if k in key_s}
                return self.db.do('users', condition=f"id={id}")[0]
            else:
                return self.db.do('users', condition=f"id={id}")[0][key_s]
        except:
            pass
        return ''

    def update_text_list(self,force=False):
        if force or not self.text_list:
            db_language = self.user('language')
            lang_cond=''
            self.lang_code=db_language
            if db_language==None or db_language==4:db_language=0
            if db_language!=None:
                lang_cond = f"language={db_language}"
            if lang_cond=='':lang_cond=None
            self.text_list = [i for i in self.db.do('texts', condition=lang_cond) if i['role']== self.role]
        return self.text_list
            
    
    def text(self, key, return_pair=False, search_by='key', return_id=False, slash=True, **kargs):
        '''
        return pair , target,id
        '''
        main_word = kargs.get('main_word')

        if key in ['',None]:return key
        if kargs.get('get_text_setting',False) and (setting_value:=self.get_setting(key)):
            return setting_value
        if not isinstance(key,str):key=str(key)
        
        if search_by == 'key' and slash and key[0] != '/':
            key = f"/{key}"
        target = 'key' if search_by == 'key' else 'value'
        pair = 'value' if search_by == 'key' else 'key'
        
        self.update_text_list(force=(self.lang_code!=self.user('language')))
        texts = [i for i in self.text_list if i[target]==key]
        if texts:
            text = texts[-1]
            if len(texts)>1 and main_word!=None:
                tmp = [i for i in texts if i[pair]==main_word]
                if tmp:
                    text = tmp[0]

            
            out = [text[pair]]
            if return_pair:
                out += [text[target]]
            if return_id:
                out += [text['id']]
            if len(out) > 1:
                return out
            return out[0]

        else:

            out = [key]
            if return_pair:
                out += [key]
            if return_id:
                out += [None]
            if len(out) > 1:
                return out
            return out[0]

    def media(self, key):
        if key == None:
            return -1, -1
        db_language = self.user('language')
        media = [i for i in self.db.do(
            'media', condition=f"language={db_language} AND key='{key}'") if i['role'] == self.role]
        if media:
            media = media[-1]
            return media['msg_id'], media['channel_id']
        return -1, -1

    ###################################################
    def get_replied_text(self):
        try:
            txt = self.update.message.reply_to_message.text
            if txt:
                return txt
            cap = self.update.message.reply_to_message.caption
            if cap:
                return cap
        except:
            pass
        return ''

    def is_replied(self):
        try:
            if self.update.message.reply_to_message != None:
                return True
        except Exception as e:
            self.log(e)
        return False

    def replace_btn_label(self, key,main_word=None):
        if isinstance(key, str):
            value, text_key = self.text(key, True,main_word=main_word,slash=False)
            if value != text_key and text_key.endswith(BTN_PFX):
                return value

            if not key.endswith(BTN_PFX):
                key += BTN_PFX
            value, text_key = self.text(key, True,main_word=main_word,slash=False)
            return value
        else:
            if not isinstance(key,list):key= list(key)
            for i in range(len(key)):
                res = self.replace_btn_label(key[i])
                if res != None:
                    key[i] = res

    def inline_keyboard_maker(self, inputs, **args):
        '''
            inputs ={key:data}

            col = args.get('col', 3)
            reverse:bool=False
            return_raw:bool=False
            add_label:bool=True
            close=True

        '''
        col = args.get('col', 3)
        reverse = args.get('reverse', False)
        add_label = args.get('add_label', True)
        return_raw = args.get('return_raw', False)
        close=args.get('close',True)
        btns = []
        for k, v in inputs.items():
            k=k.replace('*','')
            key = self.text(k,slash=False)
            if k.lower() == 'share':
                btns += [InlineKeyboardButton(key, switch_inline_query=v)]
            elif 'http://' in str(v) or 'https://' in str(v):
                btns += [InlineKeyboardButton(key, v)]
            else:
                if add_label:
                    val = f'{k}:{v}'
                else:
                    val = f'{v}'
                btns += [InlineKeyboardButton(key,
                                              callback_data=val)]
        btns = chunks(btns, col, reverse)
        if close:
            btns += [[InlineKeyboardButton('close',callback_data='close')]]   
        if return_raw:
            return btns
        return InlineKeyboardMarkup(btns)

    def btn_maker(self, btns, **args):
        '''

        return_raw:bool=False
        share_phone:bool=False ** for keyboard
        resize:bool=True ** for keyboard
        col = args.get('col', 3) ** for inline
        reverse:bool=False ** for inline


        '''
        share_phone = args.get('share_phone', False)
        return_raw = args.get('return_raw', False)
        resize = args.get('resize', True)

        if btns:
            if not isinstance(btns, (ReplyKeyboardMarkup, InlineKeyboardMarkup)):
                if isinstance(btns, list):
                    btns_list = copy.deepcopy(btns)
                    self.replace_btn_label(btns_list)
                    if return_raw:
                        return btns_list
                    share_phone = args.get('share_phone', False)
                    if share_phone:
                        btns_list[0][0] = KeyboardButton(btns_list[0][0], True)
                    return ReplyKeyboardMarkup(btns_list, resize)
                if isinstance(btns, dict):
                    return self.inline_keyboard_maker(btns, **args)

            return btns
        return None

    def setter(self):
        if Filters.text(self.update):

            text = self.get_text()
            if text == 'delete_media':
                replied = self.userdata('last_function_name')
                values = [i for i in self.db.do(
                    'media', condition=f"key='{replied}' AND language='{self.user('language')}'") if i['role'] == self.role]
                if values:
                    for i in values:
                        self.db.do('media', condition=f"id={i['id']}", delete=True)
                    self.userdata('last_function_name', delete=True)
                    self.send_message('media_deleted')
                return

            replied = self.get_replied_text()

            if replied in ['', None]:
                return
            val, key, id = self.text(
                key=replied, return_pair=True, return_id=True,slash=False)
            if not id:
                key, val, id = self.text(
                    key=replied, search_by='value', return_pair=True, return_id=True,slash=False)

            if text == 'delete_translate':
                if id:
                    self.db.do('texts', condition=f"id={id}", delete=True)
                    self.send_message('text_translate_deleted')
                else:
                    self.send_message('text_dosnt_exists')
                return
            if id:
                self.db.do(
                    'texts', {'value': text}, condition=f"id={id}")
            else:
                to_db = {
                    'id': self.time(),
                    'key': replied,
                    'value': text,
                    'language': self.user('language'),
                }
                to_db['role'] = self.role
                self.db.do('texts', to_db)
            self.send_message('text_changed')

        elif Filters.photo(self.update) or Filters.video(self.update):
            replied = self.userdata('last_function_name')
            print(replied)
            msg_id = self.send_to_host(self.get_msg_id(), self.get_chat_id())
            values = [i for i in self.db.do(
                'media', condition=f"key='{replied}' AND language='{self.user('language')}'") if i['role'] == self.role]
            if msg_id < 0:
                return -1
            if values:
                key = replied
                print(key)
                id = values[0]['id']
                self.db.do('media', {
                    'key': key,
                    'msg_id': msg_id,
                    'channel_id': self.host_channel_id,
                    'language': self.user('language'),
                    'role': self.role
                }, condition=f"id={id}")
            else:
                cfg = {'id': self.time(), 'key': replied, 'msg_id': msg_id, 'channel_id': self.host_channel_id,
                       'language':  self.user('language')}
                cfg['role'] = self.role
                self.db.do('media', cfg)
            self.userdata('last_function_name', delete=True)

            self.send('media_changed')

        self.update_text_list(force=True)
    ###################################################
    def bot_kargs(self, **kargs):
        disable_web_page_preview = kargs.get('disable_web_page_preview')
        reply_to_message_id = kargs.get('reply_to_message_id')
        parse_mode = kargs.get('parse_mode')
        disable_notification = kargs.get('disable_notification')
        entities = kargs.get('entities')
        caption_entities = kargs.get('caption_entities')
        
        out = {}
        if disable_web_page_preview:
            out['disable_web_page_preview'] = disable_web_page_preview
        if reply_to_message_id:
            out['reply_to_message_id'] = reply_to_message_id
        if parse_mode:
            out['parse_mode'] = parse_mode
        if disable_notification:
            out['disable_notification'] = disable_notification
        if entities:
            out['entities'] = entities
        if caption_entities:
            out['caption_entities'] = caption_entities
        return out

    def send(self, msg, btns=None, chat_id: int = 0, **args):
        '''
            translat = True or t=True
            slash=True
            get_text_setting:bool

            col:int
            reply_to_message_id:int,
            parse_mode:PasrMode
            disable_notification

            disable_web_page_preview:bool=False
            share_phone:bool=False
            reverse_btn:bool=False
            close:bool =True

        '''

        btn = self.btn_maker(btns, **args)
        if chat_id == 0:
            chat_id = self.id
        try:
            msg_id, host = self.media(self.userdata('last_function_name'))
            if str(msg_id) != '-1':
                return self.copy_message(
                    from_chat_id=host,
                    message_id=msg_id,
                    btns=btn,
                    caption=msg,
                    **args
                )

        except Exception as e:
            self.log(e)
        try:
            return self.send_message(
                msg=msg,
                btns=btn,
                chat_id=chat_id,
                **args
            )

        except Exception as e:
            self.log(e)
        return False

    def send_message(self, msg, btns=None, chat_id: int = 0, **args):
        '''
            translat = True or t=True
            slash=True

            col:int
            reply_to_message_id:int ,
            parse_mode:PasrMode
            disable_notification
            entites=[entity]
            caption_entities=[entity]


            disable_web_page_preview:bool=False
            share_phone:bool=False
            reverse_btn:bool=False

        '''
        args['slash'] = args.get('slash', True)
        args['translat'] = args.get('translat', True) and args.get('t',True)
        args['disable_web_page_preview'] = args.get(
            'disable_web_page_preview', True)
        btn = self.btn_maker(btns, **args)
        if chat_id == 0:
            chat_id = self.id
        if args.get('translat'):
            msg = self.text(msg, **args)
        out = self.context.bot.send_message(
            chat_id=chat_id,
            text= msg,
            reply_markup=btn,
            **self.bot_kargs(**args)
        )
        return out['message_id']
    
    def send_media(self, media:bytes,media_type:str,caption=None, btns=None, chat_id: int = 0, **args):
        '''
            media_type:photo,audio,video,document
            translat = True or t=True
            slash=True

            col:int
            reply_to_message_id:int ,
            parse_mode:PasrMode
            disable_notification
            entites=[entity]
            caption_entities=[entity]

            

            disable_web_page_preview:bool=False
            share_phone:bool=False
            reverse_btn:bool=False

        '''
        args['slash'] = args.get('slash', True)
        args['translat'] = args.get('translat', True) and args.get('t',True)
        btn = self.btn_maker(btns, **args)
        if chat_id == 0:
            chat_id = self.id
        if args.get('translat'):
            caption = self.text(caption, **args)
        if media_type=="photo":
            out = self.context.bot.send_photo(
                photo = media,
                chat_id=chat_id,
                caption= caption,
                reply_markup=btn,
                **self.bot_kargs(**args)
            )
        elif media_type=="animation":
            out = self.context.bot.send_animation(
                animation = media,
                chat_id=chat_id,
                caption= caption,
                reply_markup=btn,
                **self.bot_kargs(**args)
            )
        elif media_type=="video":
            out = self.context.bot.send_video(
                video = media,
                chat_id=chat_id,
                caption= caption,
                reply_markup=btn,
                **self.bot_kargs(**args)
            )
        elif media_type=="audio":
            out = self.context.bot.send_audio(
                audio = media,
                chat_id=chat_id,
                caption= caption,
                reply_markup=btn,
                **self.bot_kargs(**args)
            )
        elif media_type=="document":
            out = self.context.bot.send_document(
                document = media,
                chat_id=chat_id,
                caption= caption,
                reply_markup=btn,
                **self.bot_kargs(**args)
            )
        return out['message_id']

    

    def send_animation(self, photo:bytes,caption=None, btns=None, chat_id: int = 0, **args):
        '''
            translat = True or t=True
            slash=True

            col:int
            reply_to_message_id:int ,
            parse_mode:PasrMode
            disable_notification
            entites=[entity]
            caption_entities=[entity]


            disable_web_page_preview:bool=False
            share_phone:bool=False
            reverse_btn:bool=False

        '''
        args['slash'] = args.get('slash', True)
        args['translat'] = args.get('translat', True) and args.get('t',True)
        btn = self.btn_maker(btns, **args)
        if chat_id == 0:
            chat_id = self.id
        if args.get('translat'):
            caption = self.text(caption, **args)
        out = self.context.bot.send_photo(
            photo = photo,
            chat_id=chat_id,
            caption= caption,
            reply_markup=btn,
            **self.bot_kargs(**args)
        )
        return out['message_id']

    
    def copy_message(self, from_chat_id, message_id, btns=None, chat_id=0, caption=None, **args):
        '''
            translat = True or t=True
            slash=True
            col:int
            reply_to_message_id:int ,
            parse_mode:PasrMode
            disable_notification
            entites=[entity]
            caption_entities=[entity]


            disable_web_page_preview:bool=False
            share_phone:bool=False
            reverse_btn:bool=False

        '''
        args['slash'] = args.get('slash', True)
        args['translat'] = args.get('translat', True) and args.get('t',True)
        btn = self.btn_maker(btns, **args)
        if chat_id == 0:
            chat_id = self.id
        if args.get('translat'):
            caption = self.text(caption, **args)
        out = self.context.bot.copy_message(
            chat_id=chat_id,
            from_chat_id=from_chat_id,
            message_id=message_id,
            caption=caption,
            reply_markup=btn,
            **self.bot_kargs(**args)
        )
        return out['message_id']

    def edit_message_text(self, new_msg, message_id, btns=None, chat_id: int = 0, **args):
        '''
            translat = True or t=True
            slash=True
            col:int
            reply_to_message_id:int ,
            parse_mode:PasrMode
            disable_notification
            entites=[entity]
            caption_entities=[entity]


            disable_web_page_preview:bool=False
            share_phone:bool=False
            reverse_btn:bool=False

        '''
        args['slash'] = args.get('slash', True)
        args['translat'] = args.get('translat', True) and args.get('t',True)
        try:
            btn = self.btn_maker(btns, **args)
            if chat_id == 0:
                chat_id = self.id
            if args.get('translat'):
                new_msg = self.text(new_msg, **args)
            out = self.context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=new_msg,
                reply_markup=btn,
                **self.bot_kargs(**args)
            )
            return True
        except Exception as e:
            self.log(e)
        return False

    def edit_message_caption(self, new_caption, msg_id, btns=None, chat_id: int = 0, **args):
        '''
            translat = True or t=True
            slash=True

            col:int
            reply_to_message_id:int ,
            parse_mode:PasrMode
            disable_notification
            entites=[entity]
            caption_entities=[entity]


            disable_web_page_preview:bool=False
            share_phone:bool=False
            reverse_btn:bool=False

        '''
        args['slash'] = args.get('slash', True)
        args['translat'] = args.get('translat', True) and args.get('t',True)
        try:
            btn = self.btn_maker(btns, **args)
            if chat_id == 0:
                chat_id = self.id
            if args.get('translat'):
                new_caption = self.text(new_caption, **args)
            out = self.context.bot.edit_message_caption(
                chat_id=chat_id,
                message_id=msg_id,
                caption=new_caption,
                reply_markup=btn,
                **self.bot_kargs(**args)
            )
            return True
        except Exception as e:
            self.log(e)
        return False

    def edit_message_media(self, new_media, msg_id, btns=None, chat_id: int = 0, **args):
        '''
            col:int
            reply_to_message_id:int ,
            parse_mode:PasrMode
            disable_notification
            entites=[entity]
            caption_entities=[entity]


            disable_web_page_preview:bool=False
            share_phone:bool=False
            reverse_btn:bool=False

        '''
        try:
            btn = self.btn_maker(btns, **args)
            if chat_id == 0:
                chat_id = self.id
            out = self.context.bot.edit_message_media(
                chat_id=chat_id,
                message_id=msg_id,
                media=new_media,
                reply_markup=btn,
                **self.bot_kargs(**args)
            )
            return True
        except Exception as e:
            self.log(e)
        return False

    def edit_message_reply_markup(self, new_btns, msg_id, chat_id: int = 0, **args):
        '''
            col:int
            reply_to_message_id:int ,
            parse_mode:PasrMode
            disable_notification
            entites=[entity]
            caption_entities=[entity]


            disable_web_page_preview:bool=False
            share_phone:bool=False
            reverse_btn:bool=False

        '''
        try:
            btn = self.btn_maker(new_btns, **args)
            if chat_id == 0:
                chat_id = self.id

            out = self.context.bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=msg_id,
                reply_markup=btn,
                **self.bot_kargs(**args)
            )
            return True
        except Exception as e:
            self.log(e)
        return False

    def delete_message(self, msg_id, id=0):
        try:
            if id == 0:
                id = self.id
            self.context.bot.delete_message(
                chat_id=id,
                message_id=msg_id)
            return True
        except Exception as e:
            self.log(e)
            return False

    def send_to_host(self, msg_id, from_chat):
        try:
            host_channel_id = self.host_channel_id
            return self.context.bot.copy_message(message_id=msg_id, chat_id=host_channel_id, from_chat_id=from_chat)['message_id']
        except:
            self.send_message('error_copy_to_host')
        return -1

    def alarm_to_admins(self, msg, btn=None):
        try:
            for id in self.superAdmins:
                self.send(msg=msg, btns=btn, chat_id=id)
            admins = self.db.do('users', condition=f"role={Role.ADMIN.value}")

            for admin in admins:
                try:
                    if str(admin['id']) not in  [str(i) for i in self.superAdmins] and admin['status'] == 1 and (admin['get_alarm'] == 1):
                        self.send(msg=msg, btns=btn, chat_id=admin['id'])
                except Exception as e:
                    self.log(e)
        except Exception as e:
            self.log(e)

    def send_to_users(self, msg_id, chat_id, user_ids:list=None,filter_ids:list=None):
        users = self.db.do('users', condition=f"get_alarm={1} AND is_online={1}")
        if user_ids:
            users = [i for i in users if i['id'] in user_ids]
        if filter_ids:
            users = [i for i in users if i['id'] not in filter_ids]

        bot = Bot(self.super_self.token)

        for user in users:
            try:
                sleep(1)
                bot.copy_message(
                    chat_id=user['id'], from_chat_id=chat_id, message_id=msg_id)
            except Exception as e:
                e = str(e)
                if 'Flood control exceeded.' in e:
                    sleep(40)
                    try:
                        bot.copy_message(
                            chat_id=user['id'], from_chat_id=chat_id, message_id=msg_id)
                    except:
                        if 'user is deactivated' in e:
                            self.db.do(
                                'users', {'is_online': 0}, condition=f"id={user['id']}")

                if 'user is deactivated' in e:
                    self.db.do('users', {'is_online': 0},
                               condition=f"id={user['id']}")


    def send_file(self, byte_file, chat_id=0,caption=None):
        try:
            if chat_id == 0:
                chat_id = self.id
            
            self.context.bot.send_document(
                chat_id, byte_file, caption=caption)
            return True
        except Exception as e:
            self.log(e)
        return False

    def get_doc_id(self):
        return self.update.message.document.file_id
    def get_real_file_name(self):
        return self.update.message.document.file_name

    def download_file(self, file_id,path:str, file_name='',set_real_fname=True):
        '''
        return path
        '''
        try:
            bot = self.context.bot
            bot = self.bot

            file_info = bot.get_file(file_id)
            if set_real_fname:fname = self.get_real_file_name()
            else:fname = file_info.file_path.split('/')[-1].split('\\')[-1]
            fname = file_name if file_name != '' else fname
            path = path.rstrip('/')+'/'
            path += f'{fname}'
            file_info.download(path)
            return path
        except Exception as e:
            self.log(e)
        return ''

    ###################################################
    def wait(self,btns=None,delete=False):
        msg_id = self.send('wait', btns=btns)
        sleep(1)
        if delete:self.delete_message(msg_id)
        return msg_id
        

    def pagination_maker(self, items: list, per_page=5, msg_list=False,revers_list=False):
        '''
        return msg, btn

        '''
        items = chunks(list(reversed(items)), per_page)
        self.userdata('pagination_items', items)
        self.userdata('pagination_iter', 0)
        self.userdata('pagination_revers_list', revers_list)
        
        try:
            msg = self.pagination_msg_maker(msg_list)
            btn = self.pagination_btn_maker()
        except:
            msg, btn = '', []
            if msg_list:
                msg = []
        return msg, btn

    def pagination_msg_maker(self, msg_list=False):
        items = self.userdata('pagination_items')
        idx = self.userdata('pagination_iter')
        if not self.userdata('pagination_revers_list'):
            item = list(reversed(items[idx]))
        else:item = list(items[idx])
        if msg_list:
            return item
        msg = ''
        for i in item:
            msg += i
        return msg

    def pagination_btn_maker(self):
        items = self.userdata('pagination_items')
        idx = self.userdata('pagination_iter')
        if len(items) <= 1:
            return None
        else:
            total_idx = len(items)-1
            if idx == 0:
                return {'next_page': 'pagination'}
            elif idx == total_idx:
                return {'back_page': 'pagination'}
            else:
                return {'back_page': 'pagination', 'next_page': 'pagination'}

    def set_uid_inFirstRequest(self):
        try:
            print(self.update)
            # if self.id not in [0,None]:return
            # proxy = None
            # if self.bot.proxy!=None:proxy={'https':self.bot.proxy}
                
            # url = f"https://api.telegram.org/bot{self.bot.token}/getUpdates"
            # print(url)
            # data = (requests.get(url,proxies=proxy).json())
            # print(data)
            # self.bot.dp.process_update(Update.de_json(data,self.bot))
        except Exception as e:
            print(e)
    
    def check_inline_keyboards(self, txt,role:int,regex=False, *args):
        def checker(*args):
            try:
                # self.set_uid_inFirstRequest()
                item = args[0]
                if isinstance(item, str):
                    if regex:
                        return txt in item and (role == self.role or role==0)
                    else:
                        out= txt in item.split(':') and (role == self.role or role==0)
                        return out
            except:
                pass
            return False
        return checker

    def force_join_inline_filter(self):
        def checker(*args):
            try:
                channels = self.db.do('force_join')
                if len(channels) > 0:
                    for ch in channels:
                        channel_id = ch['channel_id']
                        try:
                            if not self.is_channel_member(channel_id):
                                return True
                        except Exception as e:
                            print(e)
            except Exception as e:print(e)
            return False
        return checker
    



    def is_channel_member(self, channel_id, user_id=0):
        if user_id == 0:
            user_id = self.id
        if user_id in [None,0]:return True
        try:
            status = self.context.bot.getChatMember(channel_id, user_id)['status']
            if status in ['member', 'administrator', 'creator']:
                return True
        except Exception as e:
            print(e)
        return False

    def alert(self, raw_msg, id=0,popup=False):
        if id == 0:
            id = self.update.callback_query.id
        try:
            self.context.bot.answer_callback_query(
                callback_query_id=id, text=raw_msg, show_alert=popup)
        except Exception as e:
            self.log(e)
