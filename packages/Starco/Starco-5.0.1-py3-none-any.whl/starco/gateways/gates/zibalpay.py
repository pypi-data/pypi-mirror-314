import requests,json
from zibal.zibal import zibal
from .utils import number_maker,get_random_email,Gate


class gateway(Gate):
    def __init__(self ,**kargs) -> None:
        super().__init__(**kargs)
        if self.test_mode:
            self.gate_key='zibal'
 
    def pay_link(self,**args):
        amount,callback,order_id = args.get('amount') , args.get('callback'), args.get('order_id')
        if not callback:
            callback = self.callback_maker(order_id)

        mobile,email = args.get('mobile',str(number_maker())) , args.get('email',str(get_random_email()))
        zb = zibal(self.gate_key, callback)
        amount *=10 # IRR
        request_to_zibal = zb.request(amount,mobile=mobile,description=email)
        return f"https://gateway.zibal.ir/start/{request_to_zibal['trackId']}"
    
    def verify(self,**args):
        track_id = args.get('trackId')
        callback = self.callback_maker(args.get('order_id'))
        
        zb = zibal(self.gate_key, callback)
        verify_zibal = zb.verify(track_id)
        verify_result = verify_zibal['result']
        if verify_result==100:
            return True ,args
        return False  ,args
    
   