from starco.utils import path_maker
from telegram.utils.request import Request
from telegram.ext import Defaults, Updater, Filters
from telegram.ext import MessageHandler, ConversationHandler
import json
import os
from threading import Thread
from .util.filteres import RoleFilter
from .classes import Base, Conversation
from .util.enum import ConversationNode
from telegram import Bot, Update
from starco.debug import Debug
from starco.db import DB
from .util.functions import setuper
from starco.utils.scheduler import Scheduler


class TlgBot(Bot):
    def __init__(self, BaseDirName: str, superAdmins: list[int], token: str, host_id: str = None, base_url: str = None, base_file_url: str = None, request: Request = None, private_key: bytes = None, private_key_password: bytes = None, defaults: Defaults = None, proxy: str = None, **kwargs):
        '''
            webhook_url: str = None,
            port: int = 443,
            ssl_key_path: str = None,
            ssl_cert_path: str = None,
            scheduler_status: bool = True,
            editors_id:list=[],
            respond_bad_order=True,
        '''
        os.environ['start_path'] = BaseDirName
        request_kwargs = None
        self.proxy=proxy
        if proxy:
            request_kwargs = {'proxy_url': proxy}
            request = Request(proxy_url=proxy)
        super(TlgBot, self).__init__(token, base_url, base_file_url,
                                     request, private_key, private_key_password, defaults)
        self.superAdmins: list = superAdmins
        self.webhook_inited=False
        self.host_id: list = host_id
        self.root = path_maker([])
        self.webhook_url: str = None
        self.port: int = 443
        self.ssl_key_path: str = None
        self.ssl_cert_path: str = None
        self.scheduler_status: bool = True
        self.editors_id: list = []
        self.respond_bad_order = True
        self._set_attrs(**kwargs)
        self.log = Debug(debug_mode=True, relative_path='.').debug
        self.db: DB = None
        self._tables = {}
        self._settings = {}
        self._default_db_setups()
        self.updater = Updater(self.token, use_context=True,
                               request_kwargs=request_kwargs)
        self.dp = self.updater.dispatcher
        self.bot_username = None
        self.scheduler = Scheduler(self)

    def _default_db_setups(self):
        self.add_table('users', {'id': 0, 'name': '', 'last_name': '', 'username': '', 'role': 0,'status': 0, 'phone': 0, 'language': 0, 'get_alarm': 0, 'is_online': 0, 'time': 0, 'last_seen': 0})
        self.add_table('setting', {'key': '', 'value': '', 'unit': '',
                       'type': '', 'subset': '', 'hide': 0, 'toggle': 0})
        self.add_table('texts', {'id': 0, 'key': '',
                       'value': '', 'language': 0, 'role': 0})
        self.add_table('media', {
                       'id': 0, 'key': '', 'msg_id': '', 'channel_id': '', 'language': 0, 'role': 0})
        self.add_setting('start_pm', 'سلام', subset='texts', hide=1)
        self.add_setting('bot_status', '1', type='int',
                         subset='status', hide=1)
        self.add_setting('token', self.token, subset='', hide=1)
        self.add_setting('host_id', self.host_id, subset='', hide=1)
        self.add_setting('super_admins', ','.join(
            [str(i) for i in self.superAdmins]), subset='', hide=1)
        self.add_setting('bot_username', 'Star1Vpn', subset='', hide=1)
        
    def _set_attrs(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def _get_attr(self, key):
        return self.__dict__.get(key)

    def _init_settings(self):
        setting = self.db.do('setting')
        keys = [i['key'] for i in setting]
        for k, v in self._settings.items():
            if k not in keys:
                print(f"add setting key: {k}")
                self.db.do('setting', {**{'key': k}, **v})

        setting = self.db.do('setting')
        keys = [i['key'] for i in setting]
        must_be_remove = list(set(keys) - set(self._settings.keys()))
        for k in must_be_remove:
            print(f"remove setting key: {k}")
            self.db.do('setting', condition=f"key='{k}'", delete=True)

        self.settings_subset_update()

    def add_table(self, table_name: str, keys_values: dict):
        self._tables[table_name] = {**self._tables.get(table_name, {}), **keys_values}

    def add_setting(self, key: str, value: str, subset: str = '', unit: str = '', type: str = '', hide: int = 0, toggle: int = 0):
        self._settings[key] = setuper(
            value=value, subset=subset, unit=unit, type=type, hide=hide, toggle=toggle)

    def init_db(self):
        self.db = DB(self._tables, name=self.__dict__.get(
            'db_name', 'database'), relative_path='.', debug_mode=True, debug_relative_path='.')
        self._init_settings()

    def settings_subset_update(self):
        setting_init = self._settings
        if setting_init:
            for k, v in setting_init.items():
                sub = v['subset']
                hide = v['hide']
                toggle = v['toggle']
                self.db.do('setting', {
                           'subset': sub, 'hide': hide, 'toggle': toggle}, condition=f"key='{k}'")

    def add(self, class_item: Base):

        if class_item.type == 'Conversation':
            item: Conversation = class_item
            for node in item.nodes:
                node: ConversationNode = node
                self.dp.add_handler(ConversationHandler(
                    entry_points=node.entries,
                    states=node.states,
                    fallbacks=node.fallbacks,
                    allow_reentry=node.arges.get('allow_reentry', True),
                    **node.arges
                ))
            if self._get_attr('respond_bad_order'):
                self.dp.add_handler(MessageHandler(
                    Filters.all & RoleFilter(item), item.add_method(item.not_fount)))

    def add_schedual_action(self, func, run_evry_sec: int, first_run=False):
        self.scheduler.add(
            func=func, run_evry_sec=run_evry_sec, first_run=first_run)

    def get_bot_username(self):
        self.bot_username = self.dp.bot.get_me().username
        return self.bot_username
        
    def befor_run_action(self):
        self.get_bot_username()
        self.db.do('setting',{'value':self.bot_username,'key':'bot_username'},condition="key='bot_username'")
        # self.deleteWebhook()
        print(self.bot_username)
        if self._get_attr('scheduler_status'):
            Thread(target=self.scheduler.run).start()

    def init_webhook(self):
        self.befor_run_action()
        webhook_url = self._get_attr('webhook_url')
        port = self._get_attr('port')
        if port not in [443, 80]:
            webhook_url += f':{port}'
        webhook_url += f'/webhook/{self.token}'
        self.setWebhook(webhook_url, max_connections=100)

    def run_poll(self):
        self.befor_run_action()
        self.updater.start_polling(drop_pending_updates=False)
        self.updater.idle()

    def webhook(self, json_data):
        try:
            if not self.webhook_inited:
                self.webhook_inited=True
                self.init_webhook()
            data = json.loads(json_data)
            update = Update.de_json(data, self)
            self.dp.process_update(update)
        except Exception as e:
            print(e)
