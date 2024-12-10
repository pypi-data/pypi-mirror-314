from nowpayments import NOWPayments
from nowpayments.sandbox import NOWPaymentsSandbox

class NowPayment:
    def __init__(self,api,sandbox=False) -> None:
        self.api = api
        self.payment= NOWPayments(self.api)
        if sandbox:
            self.payment=NOWPaymentsSandbox(self.api)
    
    def create_payment(self,amount:float,price_currency:str='USD',crypto = 'usdttrc20',**args):
        out = self.payment.create_payment(amount,price_currency,crypto,**args)
        return out
    def check(self,payment_id):
        return self.payment.get_payment_status(payment_id)