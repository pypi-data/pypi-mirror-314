import requests
import traceback
import json
import os
import sys
from datetime import datetime
import base64


class PanelConnctor:
    def __init__(self, link, port, password="6y2oIyGo2CA8*Su!#vY") -> None:
        self.password = password
        if link.endswith('/'):
            link = link[:-1]
        self.url = f"{link}:{port}/panel"

    def request(self,path,data):
        res=None
        res=requests.post(f"{self.url}/{path}",data=json.dumps(data),timeout=3).json()
        return res
    
    def make_service(self, remark: str, volume: float, ex_day: int):
        try:
            cfg = {
                "remark": remark,
                "volume": volume,
                "expire": ex_day,
                "password": self.password
            }
            res = self.request('create',cfg)
            return res
        except Exception as e:
            debug(e)
        return {}

    def rebuy_service(self, remark: str, volume: float, ex_day: int,name:str):
        try:
            cfg = {
                "remark": remark,
                "volume": volume,
                "expire": ex_day,
                'name':name,
                "password": self.password
            }
            res = self.request('rebuy',cfg)
            return res
        except Exception as e:
            debug(e)
        return {}

    def make_batch_service(self, remark: str, volume: float, ex_day: int,batch:int):
        try:
            cfg = {
                'batch':batch,
                "remark": remark,
                "volume": volume,
                "expire": ex_day,
                "password": self.password
            }
            res = self.request('create_batch',cfg)
            return res
        except Exception as e:
            debug(e)
        return {}

    def get_inbound_by_clients(self, remark: str,name:str=None):
        try:
            cfg = {
                "remark": remark,
                "name":name,
                "password": self.password
            }
            res = self.request('accounts',cfg)
            
            return res
        except Exception as e:
            debug(e)
        return {}

    def delete_clients(self, name: str, remark: str):
        try:
            cfg = {
                "name": name,
                "remark": remark,
                "password": self.password
            }
            res = self.request('delete_account',cfg)
            return res
        except Exception as e:
            debug(e)
        return {}

    def add_day_to_all_config(self, remark: str,extra_day:int):
        try:
            cfg = {
                "remark": remark,
                'extra_day':extra_day,
                "password": self.password
            }
            res = self.request('add_time_all_clients',cfg)
            return res
        except Exception as e:
            debug(e)
        return {}

    def add_day_to_single_config(self, remark: str,name:str,extra_day:int):
        try:
            cfg = {
                "remark": remark,
                'name':name,
                'extra_day':extra_day,
                "password": self.password
            }
            res = self.request('add_time',cfg)
            return res
        except Exception as e:
            debug(e)
        return {}

    def change_accounts(self, remark: str,names:list,extra_day:int,extra_volume:int):
        try:
            cfg = {
                "remark": remark,
                'names':names,
                'extra_volume':extra_volume,
                'extra_day':extra_day,
                "password": self.password
            }
            res = self.request('change_accounts',cfg)
            return res
        except Exception as e:
            debug(e)
        return {}
    
    def os_action(self, os_action):
        try:
            cfg = {
                "action": os_action,
                "password": self.password
            }
            res = self.request('os_action',cfg)
            return res.get('result')
        except Exception as e:
            debug(e)

    
    @staticmethod
    def sep_clients_info(info):
        try:
            clients = info['clients']
            info = {k: v for k, v in info.items() if k != 'clients'}
            clients = {i['name']: i for i in clients if 'name' in i}
            return clients, info
        except:
            pass
        return {}, {}

    @staticmethod
    def config_link_maker(name,info,alternative_link,protocol,network,security,tag='',alter_host='',alter_sni='',alter_port=0,**kwargs):
        try:
            label = kwargs.get('cfg_label')
            label = label+'-' if label!=None else ''
            clients, info = PanelConnctor.sep_clients_info(info)
            
            client = clients.get(name)
            id = client.get('id')
            base_link = info.get('remark')
            
            if info.get('panel')=='hiddify':
                host = base_link if alter_host=='' else alter_host
                base_link = alternative_link if alternative_link!='' else base_link
                if security in ['reality','tls']:
                    port = int(str(info.get(f'tls_ports')).split(',')[0])
                else:port = int(str(info.get(f'{security}_ports')).split(',')[0])
                
                path = "/"+info.get(f'path_{protocol}')+info.get(f'path_{network}')
            else:
                if alternative_link!='':
                    base_link= alternative_link
                path = info.get('wsSettings',{}).get('path','')
                port = info.get('port',0)
                network = info.get('network','')
                security = info.get('security','')
                serverName = info.get('tlsSettings',{}).get('serverName','')
                if serverName!='':base_link=serverName
                if alter_host=='':
                    host =  info.get('headers',{}).get('Host','')
                    if network=='tcp':
                        thost =  info.get('tcpSettings',{}).get('header',{}).get('request',{}).get('headers',{}).get('Host','')
                        if thost:host=thost[0]
                else:host = alter_host
                
            sni = alter_sni if alter_sni!='' else host
            tls='tls' if security=='tls' else 'none'
            if alter_port!=0:port = alter_port
            if network == 'ws':
                if protocol=='vmess':
                    out = {
                        "v": "2",
                        "ps": f"{label}{tag}",
                        "add": base_link,
                        "port": port,
                        "id": id,
                        "aid": 0,
                        "net": network,
                        "type": "none",
                        "host": host,
                        "path": path,
                        "tls": tls
                    }
                    out = json.dumps(out)
                    out = base64.b64encode(out.encode()).decode()
                    out = f"{protocol}://{out}"
                    return out
                elif protocol=='vless' or protocol=='trojan':
                    out = f"{protocol}://{id}@{base_link}:{port}?type={network}&security={tls}&alpn=http/1.1"
                    out += f"&path={path}&host={host}&fp=chrome&headerType=none"
                    if protocol=='vless':
                        out += '&encryption=none'
                    if security=='tls': out+=f"&sni={sni}"
                    out+=f"#{label}{tag}"
                    return out
            elif network == 'grpc':
                out=f"{protocol}://{id}@{base_link}:{port}?"
                if protocol in['trojan','vless']:
                    service_name = path[1:]
                    if security=='reality':
                        reality_fallback_domain = info.get('reality_fallback_domain')
                        pbk = info.get('reality_public_key')
                        sid = info.get('reality_short_ids')
                        out+=f"hiddify=1&sni={reality_fallback_domain}&type={network}&alpn=h2"
                        out+=f"&path={service_name}&serviceName={service_name}&mode=multi&encryption=none&fp=chrome"
                        out+=f"&headerType=None&security=reality&pbk={pbk}&sid={sid}"
                        out+=f"#{label}{tag}"
                        return out
                    else:
                        out+=f"security={tls}&type={network}&alpn=http/1.1"
                        out += f"&path={path}&host={host}&serviceName={service_name}&fp=chrome&headerType=none&mode=multi"
                        if protocol=='vless':
                            out += '&encryption=none'
                        if security=='tls': out+=f"&sni={sni}"
                        out+=f"#{label}{tag}"
                        return out
            elif network == 'tcp':
                if security=='reality':
                    reality_fallback_domain = info.get('reality_fallback_domain')
                    pbk = info.get('reality_public_key')
                    sid = info.get('reality_short_ids')
                    if protocol in['trojan','vless']:
                        out=f"{protocol}://{id}@{base_link}:{port}?"
                        out+=f"security=reality&alpn=h2"
                        out+=f"&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision"
                        if protocol=='vless':
                            out += '&encryption=none'
                        out+=f"&pbk={pbk}"
                        out+=f"&sid={sid}"
                        out+=f"&sni={sni}"
                        out+=f"#{label}{tag}"
                        return out
                if info.get('panel')=='xui':
                    if protocol in['trojan','vless']:
                        service_name = path[1:]
                        out=f"{protocol}://{id}@{base_link}:{port}?"
                        out += f"security=none&type={network}"
                        out += f"&path={path}&host={host}&headerType=http"
                        if protocol=='vless':
                            out += '&encryption=none'
                        out+=f"#{label}{tag}"
                        return out
                    
            
        except Exception as e:
            debug(e)
        return ''


def debug(error, debug_mode=True):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    pm = datetime.now().strftime("%H:%M") + \
        f" , {fname}:{exc_tb.tb_lineno} => "
    try:
        if not isinstance(error, str):
            err = traceback.format_exc()
            errl = err.split('\n')
            err_msg = '\n\t'.join(errl[1:])
            pm += '\n'+err_msg
        else:
            error = str(error)
            pm += '\t'+error
        PATH = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '../..'))
        with open(PATH+'/log', 'a+') as f:
            f.write(pm+'\n\n')
            if debug_mode:
                print(pm)

    except:
        pass
