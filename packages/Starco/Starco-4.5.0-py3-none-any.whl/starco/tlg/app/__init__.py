
from time import sleep, time
from telethon.sync import TelegramClient
from telethon.sync import events, functions, errors
import telethon
import os,json
from starco.debug import Debug
from starco.utils import path_maker
from .utils import *
from starco.proxy import PROXY
import nest_asyncio
from random import choice
nest_asyncio.apply()
from telethon.sessions import Session
from telethon.network.connection import Connection
from asyncio.events import AbstractEventLoop
from telethon.tl.functions.account import UpdateProfileRequest
from starco.utils import translator

class TlgApp(TelegramClient):
    def __init__(self: TelegramClient, number:str,session: str | Session, api_id: int, api_hash: str, *,  use_ipv6: bool = False, proxy=None, local_addr: str | tuple = None, timeout: int = 10, request_retries: int = 5, connection_retries: int = 5, retry_delay: int = 1, auto_reconnect: bool = True, sequential_updates: bool = False, flood_sleep_threshold: int = 60, raise_last_call_error: bool = False, device_model: str = None, system_version: str = None, app_version: str = None, lang_code: str = 'en', system_lang_code: str = 'en', loop: AbstractEventLoop = None, base_logger: str = None, receive_updates: bool = True, catch_up: bool = False, entity_cache_limit: int = 5000,auto_connect:bool=True,**kwargs):
        """
            proxy={'proxy_type':'http,socks5','ip','port','username','password'}
        """
        self.number = number
        self.log = Debug('TelegramClient').debug
        if proxy:
           proxy = PROXY(**proxy).make_proxy()
        super().__init__(
            session, api_id, api_hash,  use_ipv6=use_ipv6, proxy=proxy, local_addr=local_addr, timeout=timeout, request_retries=request_retries, connection_retries=connection_retries, retry_delay=retry_delay, auto_reconnect=auto_reconnect, sequential_updates=sequential_updates, flood_sleep_threshold=flood_sleep_threshold, raise_last_call_error=raise_last_call_error, device_model=device_model, system_version=system_version, app_version=app_version, lang_code=lang_code, system_lang_code=system_lang_code, loop=loop, base_logger=base_logger, receive_updates=receive_updates, catch_up=catch_up, entity_cache_limit=entity_cache_limit)
        
        if auto_connect:
            self.connect()
        self.d={}
        
    def do_connect(self):
        async def act():
            await self.connect()
            return True
        return self.loop.run_until_complete(act())        
    
    async def _get_status(self):
        try:
            res = await self.get_me()
        except:
            return False
        if res == None:
            return False
        return True
   
   
    def acc_status(self):
        return self.loop.run_until_complete(self._get_status())

    
    def do_login(self, first_step=False, **args):
        '''
            steps: 0=> auto
                   1=>send code 
                   2=> enter code :args= code
                   3=> enter 2fa   :args= p2fa
        '''
        
        step = self.d.get('step')
        if first_step:
            step = 0
        if step == 0:
            self.d['code'] = ''
            self.d['hash'] = ''
            self.d['p2fa'] = ''
            step = 1
        hash = args.get('hash', '')
        code = str(args.get('code', ''))
        p2fa = str(args.get('p2fa', ''))
        if step == 1:
            if self.acc_status():
                return 'session_is_active'
            out = self.loop.run_until_complete(self._send_code())
            if out[0]:
                self.d['step'] = 2
                self.d['hash'] = out[1]
                return ''
            return out[1]
        elif step == 2:
            if hash == '':
                hash = self.d.get('hash', '')
            out = self.loop.run_until_complete(self._sign_in(code, hash))
            if out[0]:
                self.d['step'] = 0
            if out[1] == 'need_pass2':
                self.d['step'] = 3
                self.d['code'] = code
                self.d['hash'] = hash
            return out[1]
        elif step == 3:
            if code == '':
                code = self.d.get('code', '')
            if hash == '':
                hash = self.d.get('hash', '')
            out = self.loop.run_until_complete(
                self._sign_in(code, hash, p2fa))
            if out[0]:
                self.d['step'] = 0
            return out[1]
        self.d['step'] = 0
        return False, 'wrong parameter in (do_login)'

    def login_loop(self):
        res = self.do_login(first_step=True)
        if res == 'session_is_active':
            # print(res)
            return
        inp = input('code:')
        while True:
            res = self.do_login(code=inp)
            if res == 'need_pass2':
                inp = input('pass2:')
                break
            elif res != '':
                # print(res)
                inp = input('code:')
            else:
                print('success login')
                return

        while True:
            res = self.do_login(p2fa=inp)
            if res != '':
                # print(res)
                inp = input('pass2:')
            else:
                print('success login')
                return
    
    def send_code(self):
        return self.loop.run_until_complete(self._send_code())

    async def _send_code(self):
        '''
            if have error session been removed
        '''
        try:
            if not await self.is_user_authorized():
                auth = await self.send_code_request(self.number)
                auth_hahs = auth.phone_code_hash
                return True, auth_hahs
            else:
                return False, '⚠️خطا در ارسال کد !'
        except errors.PhoneNumberBannedError:
            return False, f'⚠️خطا در ارسال کد به شماره {self.number} شماره شما از تلگرام مسدود شده است !'
        except errors.PhoneNumberInvalidError:
            return False, f'⚠️ شماره {self.number} اشتباه است.'
        except errors.FloodWaitError as e3:
            return False, f'⏳ شماره {self.number} از سمت تلگرام محدود شده است و تا {e3.seconds} ثانیه دیگر قابل ثبت نیست.'
        except errors.PhoneNumberOccupiedError:
            return False, '⚠️خطا در ارسال کد !'
        except errors.PhoneNumberUnoccupiedError:

            return False, '⚠️خطا در ارسال کد !'
        except ConnectionError:
            return False, '❌ارور در ارسال کد لطفا دوباره امتحان کنید.'
        except Exception as e:
            self.log(e)
            return False, '⚠️خطا در ارسال کد !'

    async def _sign_in(self, code, hash, p2fa=None):
        try:
            if not await self.is_user_authorized():
                await self.sign_in(phone=f'{self.number}', code=(code), phone_code_hash=hash)
                return True, ''
            else:
                return False, 'unknow_error'
        except errors.SessionPasswordNeededError as e:
            if p2fa:
                try:
                    await self.sign_in(password=str(p2fa))
                    return True, ''
                except Exception as e:
                    return False, "wrong_pass2"
            else:
                return False, "need_pass2"

        except errors.PhoneCodeExpiredError:

            return False, 'expied_code'
        except errors.PhoneCodeInvalidError:

            return False, 'wrong_code'
        except Exception as e:
            self.log(e)
            return False, 'unknow_error'

    async def _sign_up(self, code, hash):
        try:
            fname = 'fname'
            lname = 'lname'

            await self.sign_up(code=code, first_name=fname, last_name=lname, phone_code_hash=hash)

            return True, ''
        except errors.SessionPasswordNeededError:

            return False, "need_pass2"
        except errors.PhoneCodeExpiredError:

            return False, 'expied_code'
        except errors.PhoneCodeInvalidError:

            return False, 'wrong_code'
        except Exception as e:
            self.log(e)
            return False, 'unknow_error'

    def on_new_message(self,func,**kargs):
        '''
        func(self:TlgApp,event,**kargs)
        '''
        @self.on(event=events.NewMessage)
        @self.on(event=events.Album)
        async def action(event):
            try:
                func(self,event,**kargs)
            except Exception as e:
                print(e)

        self.run_until_disconnected()
        
    def get_all_dialogs(self):
        '''return groups entity'''
        async def act():
            ids = []
            try:
                async for dialog in self.iter_dialogs():
                    tmp = dialog.to_dict().get('entity', {})
                    ids += [tmp.to_dict()]
            except Exception as e:
                self.log(e)
            return ids
        return self.loop.run_until_complete(act())

    def just_this_sessions_is_active(self):
        async def act(self: TlgApp):
            res = False
            async with self as client:
                result = await client(functions.account.GetAuthorizationsRequest())
                current_exist = False
                for i in result.authorizations:
                    i = i.to_dict()
                    if i['current']:
                        current_exist = True
                res = len(result.authorizations) == 1 and current_exist
            return res
        return self.loop.run_until_complete(act(self))

    def do_change_or_set_2fa(self, new_p2fa: str,old_p2f=None):
        async def act():
            if old_p2f in ['',None]:
                await self.edit_2fa(new_password=new_p2fa,hint='2fa')
                return True
            else:
                if str(new_p2fa) != str(old_p2f):
                    await self.edit_2fa(str(old_p2f), new_password=new_p2fa)
                    return True
            return False

        return self.loop.run_until_complete(act())

    def change_info(self,  first_name=None, last_name=None, bio=None):
        async def act():
            await self(UpdateProfileRequest(first_name=first_name, last_name=last_name, about=bio))
            return True

        return self.loop.run_until_complete(act())
    
    def send_text(self,user,text):
        async def act():
            res = await self.send_message(user,text)
            return res
        return self.loop.run_until_complete(act())
    
    
    def get_last_message(self,entity):
        async def act():
            out = await self.get_messages(entity)
            return out[0].message
        return self.loop.run_until_complete(act())
    
    

    def get_account_status(self):
        '''
        return 'limit' , limit string time
        return 'ok' , ''
        return 'ban,''
        '''
        ban_pm='Unfortunately, some phone numbers may trigger a harsh response from our anti-spam systems'
        self.send_text('SpamBot','/start')
        sleep(2)
        last_message = self.get_last_message('SpamBot')
        if 'your account is now limited' in last_message:
            pattern = "your account is now limited until (.*?UTC)"
            stime = re.findall(pattern,last_message)[0]
            return 'limit' , stime
        elif 'Good news, no limits are currently applied to your account' in last_message:
            return 'ok',''
        elif ban_pm in last_message:
            return 'ban',''
                
    def download_by_chatId_and_fileId(self,chat_entity,file_id:int,out_path):
        async def act():
            message =await self.get_messages(chat_entity,ids=file_id)
            try:                
                if type(message.media)!=type(None):
                    out = await self.download_media(message,out_path)
                    return out
            except Exception as e:print(e)

        return self.loop.run_until_complete(act())
    
    def get_login_code(self):
        async def act():
            async for dialog in self.iter_dialogs():
                tmp = dialog.to_dict()
                if tmp.get('_') == 'Dialog' and tmp.get('name') == 'Telegram':
                    code = translator(dialog.message.message,'en')
                    # if 'Login code' in code:
                    find = re.findall('(\d{5}).',code)
                    if find:
                        return find[0],dialog.message.date
        return self.loop.run_until_complete(act())

    def logout(self):
        async def act():
            try:
                await self.log_out()
                return True
            except Exception as e:
                print(e)
                return False
        return self.loop.run_until_complete(act())
    
    def active_sessions(self):
        async def act():
            out=[]
            result = await self(functions.account.GetAuthorizationsRequest())
            for i in result.authorizations:
                    i = i.to_dict()
                    out+=[i]
            return out

        return self.loop.run_until_complete(act())
    
    def destroy_session(self,session_hash:int):
        async def act():
            try:
                await self(functions.account.ResetAuthorizationRequest(hash=int(session_hash)))
                return True
            except Exception as e:self.log(e)
            return False

        return self.loop.run_until_complete(act())

    def destroy_others_session(self):
        async def act():
            result = await self(functions.account.GetAuthorizationsRequest())
            for i in result.authorizations:
                i = i.to_dict()
                if not i['current']:
                    try:await self(functions.account.ResetAuthorizationRequest(hash=i['hash']))
                    except:pass

        return self.loop.run_until_complete(act())

    def seen_post(self, entity, ids:list[int]=[],limit=5):
        '''
            if ids==[] use limit
        '''
        async def _seen_post():
            try:
                if not ids:
                    list_of_id = []
                    async for msg in self.iter_messages(entity, limit=limit):
                        list_of_id += [int(msg.id)]
                else:list_of_id = ids
                await self(telethon.tl.functions.messages.GetMessagesViewsRequest(peer=entity, id=list_of_id, increment=True))
                return True
            except Exception as e:
                self.log(e)
            return False
            
        return self.loop.run_until_complete(_seen_post())
        
    def react_post(self, entity,reac:list, ids:list[int]=[],limit=5):
        '''
            if ids==[] use limit
            '''
        if not isinstance(reac,list):reac=[reac]
        async def _react_post():
            
            try:
                if not ids:
                    list_of_id = []
                    async for msg in self.iter_messages(entity, limit=limit):
                        list_of_id += [int(msg.id)]
                else:list_of_id = ids
                reaction=[telethon.tl.types.ReactionEmoji(
                    emoticon=choice(reac)
                )]
                for msg_id in ids:
                    await self(telethon.tl.functions.messages.SendReactionRequest(peer=entity,msg_id=msg_id,reaction=reaction))

                return True
            except Exception as e:
                self.log(e)
            return False
            
        return self.loop.run_until_complete(_react_post())
    
    def vote(self, entity, msg_id:int,option:str):
        async def act():
            try:
                await self(telethon.tl.functions.messages.SendVoteRequest(peer=entity,msg_id=msg_id,options=[option.encode()]))
                return True
            except Exception as e:
                self.log(e)
            return False
            
        return self.loop.run_until_complete(act())
    
    def join_channel(self, channel):
        async def _join_channel():
            try:
                res = await self(telethon.tl.functions.channels.JoinChannelRequest(channel))
                return True
            except Exception as e:
                self.log(e)
                return False
        return self.loop.run_until_complete(_join_channel())

    def leave_channel(self, channel):
        async def _leave_channel():
            try:
                await self(telethon.tl.functions.channels.LeaveChannelRequest(channel))
                return True
            except Exception as e:
                self.log(e)
                return False

        return self.loop.run_until_complete(_leave_channel())
    
    