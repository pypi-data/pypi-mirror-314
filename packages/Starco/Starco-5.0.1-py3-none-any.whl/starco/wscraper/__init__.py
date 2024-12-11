from functools import wraps
# from selenium import webdriver
from lib2to3.pgen2 import driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import *
# from selenium.webdriver.firefox.service import Service as FService
# from selenium.webdriver.chrome.options import Options as CHOptions
# from selenium.webdriver.firefox.options import Options as FOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from platform import system
import os
from time import sleep
from starco.utils import path_maker
from starco.pkl import Pkl
import json,zipfile

class WScraper:
    def __init__(self, name,url, browser='firefox',background=False,use_binary_location =True,profile_dirname=None,proxy=None) -> None:
        '''
        proxy ex: socks5://ip:port
        '''        
        self.url = url
        self.browser = browser
        self.background=background
        self.binary_location = use_binary_location
        self.profile_dirname =profile_dirname
        self.proxy=proxy

        self.driver = self.init_driver()
        self.pkl = Pkl(path_maker()+f'/{name}').pkl
        self.coockies = None
    
    def dec_chk_login(func):
        @wraps(func)
        def magic(self, *args, **kw):
            try:
                return func(self, *args, **kw)
            except Exception as e:
                print(e)
        return magic

    def driver_path(self):
      
        system_name = system().lower()
        base = path_maker(['drivers',f'{system_name}_{self.browser}'])
        path_maker(['drivers',f'{system_name}_{self.browser}','profile_dirname'])
        if self.browser == 'chrome':
            driver_name = 'chromedriver'
            bin_name=f'{self.browser}'
        elif self.browser == 'firefox':
            driver_name = 'geckodriver'
            bin_name=f'{self.browser}-bin'
        if  system_name== 'linux':pass
        elif system_name == 'windows':
            driver_name+='.exe'
            bin_name+='.exe'
        else:
            raise Exception('Not work on this os')
        
        

        return base , driver_name,bin_name
    
    def install_addon(self, path, temporary=None):
        # Usage: driver.install_addon('/path/to/firebug.xpi')
        # ‘self’ refers to the “Webdriver” class
        # 'path' is absolute path to the addon that will be installed
        payload = {"path": path}
        if temporary:
            payload["temporary"] = temporary
        # The function returns an identifier of the installed addon.
        # This identifier can later be used to uninstall installed addon.
        return self.driver.execute("INSTALL_ADDON", payload)["value"]

    def init_driver(self):
        base_path,driver_name ,bin_name= self.driver_path()
        print(base_path)
        if self.browser == 'chrome':
            service = ChromeService
            option = ChromeOptions
            web_driver =Chrome
        elif self.browser == 'firefox':
            service = FirefoxService
            option = FirefoxOptions
            web_driver = Firefox
            
        
        cfg= {'service':service(base_path+'/'+driver_name)}
        options:ChromeOptions = option()
        
        if self.binary_location:options.binary_location = base_path+'/'+bin_name
        if self.background:
            options.add_argument("--headless=chrome")
            options.add_argument('--no-sandbox')

        if profile_dirname:=self.profile_dirname:
            if self.browser == 'firefox':
                fp = FirefoxProfile(f'{base_path}/{profile_dirname}')
                options.profile = fp
            if self.browser == 'chrome':
                
                options.add_argument(f"--user-data-dir={base_path}/user_data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
                options.add_argument(f'--profile-directory={profile_dirname}') #e.g. Profile 3
            options.add_argument("--enable-javascript")
            options.add_argument("--ignore-certificate-errors")
        if proxy:=self.proxy:
            print(f"{proxy=}")
            options.add_argument(f"--proxy-server={proxy['proxy_type']}://{proxy['ip']}:{proxy['port']}")
        cfg['options']=options
        return web_driver(**cfg)
    
    def proxy_plugin(self,PROXY_HOST,PROXY_PORT,PROXY_USER,PROXY_PASS):
        print('install proxy extention')
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 3,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "storage",
                "declarativeNetRequest"
            ],
            "background": {
                "scripts"   : ["background.js"]
            },
            "host_permissions": [
                "<all_urls>"
  ],
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
  mode: "fixed_servers",
  rules: {
    singleProxy: {
      scheme: "socks5",
      host: "89.58.58.42",
      port: parseInt(1080)
    },
    bypassList: ["<local>"]
  }
};

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
  return {
    authCredentials: {
      username: "starco",
      password: "1234"
    }
  };
}

chrome.webRequest.onAuthRequired.addListener(
  callbackFn,
  {urls: ["<all_urls>"]},
  ['blocking']
);
        """ 
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        return pluginfile
    
    def save_cookies(self):
        self.pkl('cookies', self.driver.get_cookies())
    
    def save_local_storage(self):
        self.pkl('local_storage', self.driver.execute_script("return window.localStorage;"))
    

    def load_local_storage(self):
        local_storage = self.pkl('local_storage', empty_return={})
        for k,v in local_storage.items():
            if v:
                self.driver.execute_script(f"window.localStorage.setItem('{k}',{json.dumps(v)});")
        self.load_url()

    def load_cookies(self):
        cookies = self.pkl('cookies', empty_return=[])
        if len(cookies) > 0:
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    print(cookie)
            self.coockies = cookies
            self.load_url()

    def check_page_loaded(self,wait_sec=15,by =By.CSS_SELECTOR,element='html'):
        WebDriverWait(self.driver, wait_sec).until(EC.element_to_be_clickable((by,element)))
        
    def check_element(self, by:By, element):
        try:
            self.driver.find_element(by, element)
            return True
        except:
            pass
        return False
   
    def load_url(self,url=''):
        if url =='':url =self.url
        self.driver.get(url)
        self.check_page_loaded()
       
    def fill_input(self,by:By,targe:str,value:str):
        elem = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((by, targe)))
        return elem.send_keys(value)
    
    def click(self,by:By,targe:str):
        elem = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((by, targe)))
        return elem.click()
    
    
    def get_text(self,by:By,targe:str):
        elem = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((by, targe)))
        return elem.text
    def get_html(self,by:By,targe:str):
        elem = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((by, targe)))
        return elem.get_attribute('innerHTML')
     
    def get_class(self,by:By,targe:str,clickable=True):
        return self.get_attr(by,targe,'class',clickable)
    
    def get_attr(self,by:By,targe:str,attr,clickable=True):
        if clickable:
            elem = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((by, targe)))
        else:elem =self.driver.find_element(by, targe)
        return elem.get_attribute(attr)


    def clear_storage(self,storage_type='local'):
        '''
            storage_type='loacal , session'
        '''
        self.driver.execute_script(f"window.{storage_type}Storage.clear();")

    def set_storage(self,data:dict,storage_type='local'):
        '''
            storage_type='loacal , session'
        '''
        for k,v in data.items():
            if v:
                self.driver.execute_script(f"window.{storage_type}Storage.setItem('{k}', '{v}');")
    
    def get_storage(self,storage_type='local'):
        '''
            storage_type='loacal , session'
        '''
        return self.driver.execute_script(f"return window.{storage_type}Storage;")
    