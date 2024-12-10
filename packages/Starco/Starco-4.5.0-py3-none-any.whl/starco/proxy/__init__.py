import ssl
from python_socks.sync import Proxy  as proxy
import certifi
import python_socks

class PROXY:
    def __init__(self,proxy_type:str,ip:str,port:int,username:str=None,password:str=None,timeout=5) -> None:
        '''
            proxy_type:str
            http , socks4 ,socks5
        '''
        if proxy_type not in ['http' , 'socks4' ,'socks5']:
            raise Exception('wrong proxy_type')
        self.proxy_type = proxy_type
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout
    def make_proxy(self):
        out = {}
        if self.proxy_type == 'http':
            proxy_type = python_socks.ProxyType.HTTP
        elif self.proxy_type == 'socks4':
            proxy_type = python_socks.ProxyType.SOCKS4
        elif self.proxy_type == 'socks5':
            proxy_type = python_socks.ProxyType.SOCKS5
        out['proxy_type'] = proxy_type
        out['addr'] = self.ip
        out['port'] = int(str(self.port))
        if self.username:out['username'] = self.username
        if self.password:out['password'] = self.password
        return out
    
    def _str_proxy(self):
        out= f"{self.proxy_type}://"
        if self.username and self.password:
            out+= f"{self.username}:{self.password}@"
        out+= f"{self.ip}:{self.port}"
        return out
    
    def check(self):
        str_proxy = self._str_proxy()
        print(f"checking {str_proxy}...")
        try:
            p = proxy.from_url(str_proxy)

            # `connect` returns standard Python socket in blocking mode
            sock = p.connect(dest_host='check-host.net', dest_port=443,timeout=self.timeout)
            sock = ssl.create_default_context(cafile=certifi.where()).wrap_socket(
                sock=sock,
                server_hostname='check-host.net'
            )
            
            request = (
                b'GET /ip HTTP/1.1\r\n'
                b'Host: check-host.net\r\n'
                b'Connection: close\r\n\r\n'
            )
            sock.sendall(request)
            response = sock.recv(4096)
            return True
        except Exception as e:
            print(e)
            return False
        

