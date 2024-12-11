
from starco.tlg.bot import TlgBot
import random
from starco.proxy import PROXY

def get_proxies(self:TlgBot):
    try:
        if self.db.do('setting', condition=f"key='proxy_status'")[0]['value']!='1':return []
        proxies = self.db.do('setting', condition=f"key='proxies'")[0]['value']
        proxies = [i.strip() for i in proxies.split('\n') if i not in ['','0', None]]
        return proxies
    except Exception as e:
        print(e)
    return []
def get_active_proxy(self:TlgBot):
    proxies=get_proxies(self)
    if proxies:
        random.shuffle(proxies)
        for proxy in proxies:
            prx = PROXY(**PROXY.str_to_dict(proxy))
            if prx.check():
                return prx._str_proxy()
    return None
    