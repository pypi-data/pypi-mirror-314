import importlib


class Gateway:
    def __init__(self,gate_name:str,base_callback_url:str,gate_key:str,test_mode:bool=False,**kargs) -> None:
        '''
        'callback_method':str defualt set
        '''
        if gate_name not in Gateway.gates_list():
            raise Exception('wrong gate name')
        path = f'starco.gateways.gates.{gate_name}'
        print(path)
        mod = importlib.import_module(path)
        self.gate = getattr(mod, 'gateway')(base_callback_url=base_callback_url,gate_key=gate_key,test_mode=test_mode,**kargs)
    
    @staticmethod
    def gates_list():
        return ['aqayepardakht','vandar','zibalpay','idpay','nextpay']
    def pay_link(self,amount:float,order_id:str=None,callback:str=None,**kargs):

        '''
            *idpay,nextpay=> need order_id*
        
            amount:toman

            callback or order_id must be filled

            mobile , email
        '''
        return self.gate.pay_link(amount=amount,callback=callback,order_id=order_id,**kargs)
    def verify(self,**kargs):
        '''
            aqayepardakht:amount,transid
            vandar       : token
            zibal        :track_id,order_id
            idpay        :id,order_id
            nextpay      :amount,trans_id

            return status,kargs
        '''
        return self.gate.verify(**kargs)

if __name__ == "__main__":
    g = Gateway('aqayepardakht','',True)
    pl = g.pay_link(1000,'https://test.ir')
    print(pl)
