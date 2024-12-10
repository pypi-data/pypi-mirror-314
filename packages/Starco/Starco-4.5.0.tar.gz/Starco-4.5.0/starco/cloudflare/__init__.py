import CloudFlare
class CloudFlareHandler:
    def __init__(self,email,api) -> None:
        self.cf = CloudFlare.CloudFlare(email,token=api)
    def get_dns_records(self,domain):
        params = {'name': domain}
        zones = self.cf.zones.get(params=params)
        zone = [i for i in zones if i['name']==domain]
        if not zone:
            raise Exception('domain not exists')
        zone_id = zone[0]['id']
        dns_records = self.cf.zones.dns_records.get(zone_id)
        return dns_records
        
    def update_dns_records(self,domain,sub,record_type,new_content=None,new_type=None,proxy:bool=None):
        record_type = record_type.upper()
        if new_type:new_type.upper()
        params = {'name': domain}
        zones = self.cf.zones.get(params=params)
        zone = [i for i in zones if i['name']==domain]
        if not zone:
            raise Exception('domain not exists')
        zone_id = zone[0]['id']
        if '.' not in sub:sub=sub+f".{domain}"
        
        dns_records = self.cf.zones.dns_records.get(zone_id)
        dns_records = [i for i in dns_records if i['name']==sub and i['type']==record_type]
        if not dns_records:
            raise Exception('dns_records not exists')
        record = dns_records[0]
        if not new_content:new_content=record['content']
        if not new_type:new_type=record['type']
        
        data={'name':record['name'],'content':new_content,'type':new_type,}
        if proxy!=None:
            data['proxied']=proxy
        
        self.cf.zones.dns_records.put(zone_id,record['id'],data=data)
        if self.purge_cache(zone_id):
            return True
        raise Exception('cache dont be purged')
    
    def purge_cache(self,zone_id=None,domain=None):
        if not zone_id and not domain:
            raise Exception('fill one of inputs parameters')
        if not zone_id:
            params = {'name': domain}
            zones = self.cf.zones.get(params=params)
            zone = [i for i in zones if i['name']==domain]
            if not zone:
                raise Exception('domain not exists')
            zone_id = zone[0]['id']
        
        self.cf.zones.purge_cache.post(zone_id,data={'purge_everything':True})
        return True
        
    def delete_dns_records(self,domain,sub,record_type):
        record_type = record_type.upper()
        params = {'name': domain}
        zones = self.cf.zones.get(params=params)
        zone = [i for i in zones if i['name']==domain]
        if not zone:
            raise Exception('domain not exists')
        zone_id = zone[0]['id']
        if '.' not in sub:sub=sub+f".{domain}"
        
        dns_records = self.cf.zones.dns_records.get(zone_id)
        dns_records = [i for i in dns_records if i['name']==sub and i['type']==record_type]
        if not dns_records:
            raise Exception('dns_records not exists')
        record = dns_records[0]
        
        self.cf.zones.dns_records.delete(zone_id,record['id'])
        if self.purge_cache(zone_id):
            return True
        raise Exception('cache dont be purged')
        
    def add_dns_records(self,domain,sub,record_type,content,proxy:bool=None):
        record_type = record_type.upper()
        params = {'name': domain}
        zones = self.cf.zones.get(params=params)
        zone = [i for i in zones if i['name']==domain]
        if not zone:
            raise Exception('domain not exists')
        zone_id = zone[0]['id']
        if '.' not in sub:sub=sub+f".{domain}"
        
        
        
        data={'name':sub,'content':content,'type':record_type}
        if proxy!=None:
            data['proxied']=proxy
        
        self.cf.zones.dns_records.post(zone_id,data=data)
        return True
    
    def get_all_domain(self):
        cf = self.cf
        zones = cf.zones.get()
        return [i['name'] for i in zones]


import ipaddress

def dns_type_detection(ip_or_domain):
    try:
        ip = ipaddress.ip_address(ip_or_domain)
        return 'A'
    except:
        return 'CNAME'

    