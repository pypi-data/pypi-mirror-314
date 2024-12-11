import requests,json
from .utils import number_maker,get_random_email,Gate

class gateway(Gate):
    def __init__(self ,**kargs) -> None:
        super().__init__(**kargs)
        if self.test_mode:
            self.gate_key='b11ee9c3-d23d-414e-8b6e-f2370baac97b'

 
    def pay_link(self,**args):
        amount,callback,order_id = args.get('amount') , args.get('callback'), args.get('order_id')
        if not callback:
            callback = self.callback_maker(order_id)
        mobile,email = args.get('mobile',str(number_maker())) , args.get('email',str(get_random_email()))
        payload=f'api_key={self.gate_key}&amount={amount}&customer_phone={mobile}&payer_desc={email}&order_id={order_id}&callback_uri={callback}&auto_verify=yes'
        headers = {
        'User-Agent': 'PostmanRuntime/7.26.8',
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        url = "https://nextpay.org/nx/gateway/token"
        
        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        json_data = json.loads(response.text)
        if response.status_code == 200 and str(json_data['code']) == '-1':
            return f"https://nextpay.org/nx/gateway/payment/{json_data['trans_id']}"
        return None            
    
    def verify(self,**args):
        amount,trans_id = args.get('amount') , args.get('trans_id')
        url = "https://nextpay.org/nx/gateway/verify"

        payload=f'api_key={self.gate_key}&trans_id={trans_id}&amount={amount}'
        headers = {
        'User-Agent': 'PostmanRuntime/7.26.8',
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        json_data = json.loads(response.text)
        if response.status_code == 200 and str(json_data['code']) == '0':
            return True ,args
        return False  ,args