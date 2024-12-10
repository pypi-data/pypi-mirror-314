import requests,json
from .utils import number_maker,get_random_email,Gate

class gateway(Gate):
    def __init__(self ,**kargs) -> None:
        super().__init__(**kargs)
        if self.test_mode:
            self.gate_key='6a7f99eb-7c20-4412-a972-6dfb7cd253a4'

    def pay_link(self,**args):
        amount,callback,order_id = args.get('amount') , args.get('callback'), args.get('order_id')
        if not callback:
            callback = self.callback_maker(order_id)

        amount*=10
        mobile,email = args.get('mobile',str(number_maker())) , args.get('email',str(get_random_email()))
        url = 'https://api.idpay.ir/v1.1/payment'
        data = {
            'order_id': order_id,
            'amount': amount,
            'callback': callback,
            'phone':mobile,
            'mail':email
            
        }
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': self.gate_key,
            'X-SANDBOX': '1' if self.test_mode else '0'
        }
        request = requests.post(url, data = json.dumps(data), headers = headers,timeout=20)
        print(request.text)
        if request.status_code == 201:
            return request.json()['link']


    def inquiry(self, id, order_id):

        url = 'https://api.idpay.ir/v1.1/payment/inquiry'

        data = {
            'id': id,
            'order_id': order_id,
        }

        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': self.gate_key,
            'X-SANDBOX': '1' if self.test_mode else '0'
        }

        request = requests.post(url, data=json.dumps(data), headers=headers,timeout=20)

        if request.status_code == 200:
            return True

        return False

    
    def verify(self,**args):
        id,order_id = args.get('id') , args.get('order_id')
        
        url = 'https://api.idpay.ir/v1.1/payment/verify'
        data = {
            'id': id,
            'order_id': order_id,
        }

        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': self.gate_key,
            'X-SANDBOX': '1' if self.test_mode else '0'
        }

        request = requests.post(url, data=json.dumps(data), headers=headers,timeout=20)
        try:args['amount'] = float(args['amount'])/10
        except:pass
        if request.status_code == 200:
            return self.inquiry(id,order_id) ,args
        return False ,args








# class IDPayAPI:

#     def __init__(self, api_key, domain, sandbox = False):
#         self.api_key = api_key
#         self.domain = domain
#         self.sandbox = sandbox


#     def payment(self, order_id, amount, callback_page, payer = {}):

     
#     def verify(self, id, order_id):




#     
#     def get_status(self, status):

        states = {
            1: 'Transaction created',
            2: 'Transaction failed',
            3: 'An error has occurred',
            4: 'Transaction blocked',
            5: 'Transaction rejected to payer',
            6: 'Transaction rejected',
            7: 'Transaction canceled',
            8: 'Redirected to IPG',
            10: 'Verify pending',
            100: 'Transaction verified',
            101: 'Verified again',
            200: 'Transaction settled',
        }

        if states[int(status)]:
            return states[int(status)]

        return False