from hcloud import Client
from hcloud.images.client import Image
from hcloud.locations.client import Location
from hcloud.server_types.client import ServerType
from hcloud.networks.client import Network
from hcloud.datacenters.client import Datacenter
from hcloud.servers.client import Server
from hcloud.primary_ips.client import PrimaryIP
from time import time, sleep


class Hetzner:
    def __init__(self, token,**kargs) -> None:
        self.client = Client(token=token,**kargs)
        self.locations = ['fsn1', 'nbg1', 'hel1', 'hil', 'ash']
        self.datacenters = ['fsn1-dc14', 'nbg1-dc3', 'hel1-dc2']
        
        self.image_names = ['ubuntu-22.04']
        self.plans = ['cx11','cpx11','cx21']

    def create_server(self, name='', plan="cx11", image_name='ubuntu-22.04', location="nbg1"):
        '''
        return server and root password
        '''
        if name == '':
            name = f"Server{int(time())}"
        res = self.client.servers.create(
            name=name,
            server_type=ServerType(name=plan),
            image=Image(name=image_name),
            location=Location(name=location)
            
        )
        return res.server, res.root_password

    def delete_server(self, id):
        self.client.servers.delete(Server(id=id))
        return True
    
    def get_all_servers(self):
        return [i.__dict__['data_model'] for i in self.client.servers.get_all()]

    def power_off(self, id):
        self.client.servers.power_off(Server(id=id))
        return True

    def power_on(self, id):
        self.client.servers.power_on(Server(id=id))
        return True

    def reset_password(self, id):
        return self.client.servers.reset_password(Server(id=id)).root_password

    def reboot(self, id):
        self.client.servers.reboot(Server(id=id))
        return True

    def rebuild(self, id, image_name):
        self.client.servers.rebuild(Server(id=id), Image(name=image_name))
        return True

    def get_all_primary_ips(self):
        return [i.__dict__['data_model'] for i in self.client.primary_ips.get_all()]
    
    def get_primary_ips_by_id(self,id):
        inf = self.client.primary_ips.get_by_id(id=id)
        return inf
    
    def get_server_by_id(self,server_id):
        return self.client.servers.get_by_id(server_id).data_model
        
    def create_primary_ips(self,datacenter_name):
        name = f'ip{int(time())}'
        self.client.primary_ips.create('ipv4',Datacenter(name=datacenter_name),name)
        return True
    
    def delete_primary_ips(self, id):
        self.client.primary_ips.delete(PrimaryIP(id))
        return True

    def lock_primary_ips(self, id):
        self.client.primary_ips.change_protection(PrimaryIP(id), True)
        return True

    def unlock_primary_ips(self, id):
        self.client.primary_ips.change_protection(PrimaryIP(id), False)
        return True

    def delete_ipv6_from_server(self,server_id):
        self.power_off(server_id)
        sleep(10)
        server_info = self.client.servers.get_by_id(server_id)
        sleep(2)
        primary_ipv6 = server_info.public_net.primary_ipv6
        if type(primary_ipv6)!=type(None):
            self.client.primary_ips.unassign(primary_ipv6)
            sleep(2)
        self.delete_primary_ips(primary_ipv6.id)
        sleep(5)
        self.power_on(server_id)
        return True

    def change_server_ip(self,server_id,ip_id):
        print("turning off")
        for _ in range(10):
            server_info = self.client.servers.get_by_id(server_id)
            if server_info.status!='off':
                try:self.power_off(server_id)
                except:pass
            else:break
            sleep(3)
        else:raise Exception(f"/hsrv{server_id} cant be power off")

        # unassign ip
        print("unassign ip")

        old_ip = None
        for _ in range(10):
            server_info = self.client.servers.get_by_id(server_id)
            primary_ipv4 = server_info.public_net.primary_ipv4
            print(primary_ipv4)
            if type(primary_ipv4)!=type(None):
                try:
                    old_ip = server_info.public_net.ipv4.ip
                    self.client.primary_ips.unassign(primary_ipv4)
                except:pass
            else:break
            sleep(3)
        else:raise Exception(f"/hsrv{server_id} cant unassign ip")

        # create ip
        print("create ip")
        try:
            if ip_id==0:
                new_ip_name= f'ip{int(time())}'
                primary_ip = self.client.primary_ips.create('ipv4',datacenter=server_info.datacenter,name=new_ip_name).primary_ip
            else:primary_ip = self.get_primary_ips_by_id(ip_id)
        except Exception as e:
            raise Exception(f"/hsrv{server_id} cant create ip")

        print("assign new ip")
        for _ in range(10):
            server_info = self.client.servers.get_by_id(server_id)
            primary_ipv4 = server_info.public_net.primary_ipv4
            if type(primary_ipv4)==type(None):
                try:
                    self.client.primary_ips.assign(primary_ip,server_id)
                except Exception as e:print(e)
            else:break
            sleep(3)
        else:raise Exception(f"/hsrv{server_id} cant assign new ip")

        print("turning on")
        for _ in range(10):
            server_info = self.client.servers.get_by_id(server_id)
            if server_info.status!='running':
                try:self.power_on(server_id)
                except:pass
            else:break
            sleep(5)
        else:raise Exception(f"/hsrv{server_id} cant turning on")

        return old_ip
    
    def assign_to_server(self,ip_id,server_id):
        self.power_off(server_id)
        sleep(10)
        server_info = self.client.servers.get_by_id(server_id)
        sleep(2)
        primary_ipv4 = server_info.public_net.primary_ipv4
        if type(primary_ipv4)!=type(None):
            self.client.primary_ips.unassign(primary_ipv4)
            sleep(2)
        self.client.primary_ips.assign(PrimaryIP(id=ip_id),server_id)
        sleep(5)
        self.power_on(server_id)
        return True
        
    def unassign_from_server(self,ip_id):
        info = self.get_primary_ips_by_id(ip_id)
        assing_id = info.assignee_id
        if assing_id!=None:
            server_id = info.assignee_id
            self.power_off(server_id)
            sleep(10)
            self.client.primary_ips.unassign(PrimaryIP(id=ip_id))
        return True
    
    def batch_ip4_creator(self,datacenter_name,count):
        success=0
        for i in range(count):
            try:
                new_ip_name= f'ip{int(time())}'
                self.client.primary_ips.create('ipv4',datacenter=Datacenter(name=datacenter_name),name=new_ip_name)
                success+=1
            except:pass
            sleep(10)
        return success
    
    def floating_ips(self):
        return self.client.floating_ips.get_all()

    def add_float_ip(self,ip_name,loacation_name,type='ipv4'):
        return self.client.floating_ips.create(type,home_location=Location(name=loacation_name),name=ip_name)
        




    
if __name__ == "__main__":
    token = '9Ii0sFqfxOZX3K4mGjIpGMxDHEJfyFjJ9rRGySNm7hRyJaJwK3ncbOwh9hx0FNLb'
    h = Hetzner(token)
    # id=35188187
    
    # for i in h.get_all_servers():
    #     print(f"{i.datacenter.__dict__}")
    #     break
    # h.change_server_ip(id)
    # Server().status

    # print(h.create_server())
    # sid = 35188187
    # print(h.power_on(sid))
    # print(h.reboot(sid))
    # print(h.reset_password(sid))
    # print(h.rebuild(sid,h.image_names[0]))
    # h.delete_primary_ips(id)
    
    # for i in h.get_all_primary_ips():
    #     print(i)

    # o = h.delete_server(35187409)
    # print(o)
