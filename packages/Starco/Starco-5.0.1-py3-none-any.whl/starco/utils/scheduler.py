    
from time import time,sleep

class Scheduler:
    def __init__(self,super_self) -> None:
        self.super_self = super_self
        self.schecdaul_info={}

    def allow(self,name):
        now = int(time())
        item = self.schecdaul_info.get(name,{})
        last_run = item.get('last_run',0)
        first_run = item.get('first_run',0)
        run_evry_sec = item.get('run_evry_sec',0)
        if last_run==0:
            self.schecdaul_info[name]['last_run']=now
            if first_run:
                return True
        else:
            if now%run_evry_sec==0 or now - last_run > run_evry_sec:
                self.schecdaul_info[name]['last_run']=now
                return True
                
        return False

    def add(self,func,run_evry_sec:int,first_run=False):
        '''
            function with input self
        '''
        name = str(func.__name__)
        self.schecdaul_info[name] = {'func':func,'run_evry_sec':run_evry_sec,'first_run':first_run,'last_run':0}
    
    def run(self):
        while True:
            for name , dict_val in self.schecdaul_info.items():
                try:
                    if self.allow(name):
                        dict_val['func'](self.super_self)
                except Exception as e:self.super_self.debug.debug(e)
            sleep(1)

