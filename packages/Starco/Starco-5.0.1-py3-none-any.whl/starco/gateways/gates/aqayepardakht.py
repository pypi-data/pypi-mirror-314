import requests,json
from .utils import number_maker,get_random_email,Gate


class gateway(Gate):
    def __init__(self ,**kargs) -> None:
        super().__init__(**kargs)
        if self.test_mode:
            self.gate_key='sandbox'
 
    def pay_link(self,**args):
        amount,callback,order_id = args.get('amount') , args.get('callback'), args.get('order_id')
        if not callback:
            callback = self.callback_maker(order_id)

        mobile,email = args.get('mobile',str(number_maker())) , args.get('email',str(get_random_email()))
        data = {
            'pin' : self.gate_key ,
            'amount' : amount,
            'callback' : callback,
            'mobile':mobile,
            'email':email
            }
        response = requests.post('https://panel.aqayepardakht.ir/api/v2/create', data = data,timeout=20)
        json_data = json.loads(response.text)
        if response.status_code == 200 and json_data['status'] == 'success':
            path = 'startpay'
            if self.test_mode:path='startpay/sandbox'
            return f'https://panel.aqayepardakht.ir/{path}/'+json_data['transid']
        return None            
    
    def verify(self,**args):
        amount,transid = args.get('amount') , args.get('transid')
        data = {
            'pin' : self.gate_key,
            'amount' : amount,
            'transid' : transid
        }

        response = requests.post('https://panel.aqayepardakht.ir/api/v2/verify', data = data,timeout=20)
        json_data = json.loads(response.text)
        print(json_data)
        if response.status_code == 200 and str(json_data['code']) == '1':
            return True ,args
        return False  ,args