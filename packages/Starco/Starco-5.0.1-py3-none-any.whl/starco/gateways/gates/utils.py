
from random import choice,randint
import os

def number_maker():
        pidh = ['911','912','933','936','937','938','939','902','990']
        number = f"0{choice(pidh)}{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}"
        return number
    
def get_random_email():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__)))+'/emails.txt'
    with open(path , 'r') as f:
        res = f.read()
    return choice(res.split('\n'))
 



class Gate:
    def __init__(self,gate_key,test_mode,**kargs) -> None:
        self.gate_key = gate_key
        self.test_mode = test_mode
        callback_path = 'callback'
        base_callback_url:str = kargs.get('base_callback_url')
        print(base_callback_url)
        self.callback = base_callback_url.rstrip('/')+f"/{callback_path}/"+"{}"

        for k,v in kargs.items():
            self.__dict__[k]=v
    
    def callback_maker(self,order_id):
        return self.callback.format(str(order_id))
         
    def pay_link(self,**kargs):
        '''must be overriding'''
        pass
    def verify(self,**kargs):
        '''must be overriding'''
        pass