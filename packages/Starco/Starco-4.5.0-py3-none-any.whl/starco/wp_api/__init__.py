import requests,os
from starco.debug import Debug
from time import sleep
class WpApi:
    def __init__(self,username:str,password:str,site_url:str) -> None:
        ''''
            site_url = https://your_site.com
        '''
        self.username = username
        self.password = password
        self.site_url = site_url.rstrip('/')+'/'
        self.token=None
        self.status = False
        self.init_token()  
        self.debug = Debug(relative_path='.')
    
    def check_token(self):
        res = self.req('posts',get=True)
        if res.status_code==200:return True
        return False
    
    def fetch_token(self):
        try:
            data = {
                'username':self.username,
                'password':self.password
            }
            res= self.req('token',data,'api/v1',False).json()
            self.token = res['jwt_token']
        except:pass
        
    def req(self,end_point:str,data:dict=None,end_point_pfx='wp/v2',set_header = True,get=False):
        try:
            # posts
            headers=None
            if set_header:
                headers = {
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                }
            url = self.site_url+f'wp-json/{end_point_pfx}/{end_point}'
            if get:
                return requests.get(url,json=data,headers=headers,timeout=10)
            return requests.post(url,json=data,headers=headers,timeout=10)
        except Exception as e:
            self.debug.debug(e)
    def init_token(self):
        path='.token'
        if os.path.exists(path):
            with open(path,'r') as f:
                self.token = f.read()
            if self.check_token():
                self.status=True
                return        
        self.fetch_token()
        if self.check_token():
            with open('.token','w') as f:
                f.write(self.token)
            self.status=True
            return 
        
    def posts(self,title=None,content=None,status='publish',**args):
        '''
            *if any parameters dont be fill return all posts
            featured_media:int
            tags:list:str
            categories:list:str
        '''
        if title:
            data = {
                "title": title,
                "content": content,
                "status": status
            }
            tags=args.get('tags',[])
            categories=args.get('categories',[])
            featured_media=args.get('featured_media')
            
            if tags:
                o_tags=[]
                for i in tags:
                    o_tags+=self.meta(i,type='tags')
                if o_tags:
                    data['tags'] = o_tags
            if categories:
                o_categories=[]
                for i in categories:
                    o_categories+=self.meta(i,type='categories')
                    
                if o_categories:
                    data['categories'] = o_categories
            if featured_media:
                data['featured_media'] = featured_media
            res= self.req('posts',data)
        else:
            res= self.req('posts',get=True)
        return res
    
    def meta(self,name:str=None,type='tags'):
        '''
            type =['tags','categories']
            *if any parameters dont be fill return all type
            else return id
        '''
        name = name.strip()
        try:
            if name:
                o= self.req(type,data={'search':name},get=True)
                o = [i['id'] for i in o.json() if i['name']==name]
                if o:return o
                data = {
                    "name": name,
                }
                res= self.req(type,data)
                return [res.json()['id']]
            else:
                res= self.req(type,get=True)
            return res
        except Exception as e:
            self.debug.debug(e)
            return []

if __name__ == "__main__":
    cls = WpApi(
        'manmodiram',
        'XGwr&25htW$G(Y1uhC',
        'http://starco.fun',
    )
    
            
    o =cls.posts('title۲۲','test۲۳۴۵۶۴',categories=['کانفیگ رایگان V2ray'])
    # o=[i['id'] for i in o.json() if i['name']=='test']
    print(o.json())


# response = requests.post(url, json=data, headers=headers)


