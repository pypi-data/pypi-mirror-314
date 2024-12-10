import requests,json
from .utils import number_maker,get_random_email,Gate



class gateway(Gate):
    def __init__(self ,**kargs) -> None:
        super().__init__(**kargs)
 
    def pay_link(self,**args):
        amount,callback,order_id = args.get('amount') , args.get('callback'), args.get('order_id')
        if not callback:
            callback = self.callback_maker(order_id)

        mobile,email = args.get('mobile',str(number_maker())) , args.get('email',str(get_random_email()))

        data = {
            'api_key' : self.gate_key ,
            'amount' : amount*10,
            'callback_url' : callback,
            'mobile_number':mobile,
            'comment':email
            }

        headers= {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data =  json.dumps(data)
        response = requests.post('https://ipg.vandar.io/api/v3/send', data =data,headers=headers)

        json_data = json.loads(response.text)
        print(json_data)
        if response.status_code == 200 and str(json_data['status']) == '1':
            token = json_data['token']
            return f"https://ipg.vandar.io/v3/{token}"
        return None            
    
    def verify(self,**args):
        token = args.get('token')
        
        data = {
            'api_key' : self.gate_key,
            'token' : token
        }
        headers= {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data =  json.dumps(data)
        response = requests.post('https://ipg.vandar.io/api/v3/verify', data = data,headers=headers)
        json_data = json.loads(response.text)
        if response.status_code == 200 and str(json_data['status']) == '1':
            return True ,args
        return False  ,args