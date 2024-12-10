import requests
import sys,os
import traceback
from datetime import datetime
from..utils.directories import path_maker
from telegram import Bot
class Debug:
    def __init__(self,debug_mode=True,relative_path='',log_name='log',token=None,tlg_id=None,alarm_mode=True) -> None:
        self.debug_mode = debug_mode
        self.relative_path= relative_path
        self.log_name =log_name
        self.token=token
        self.tlg_id=tlg_id
        self.alarm_mode=alarm_mode
        
    def alarm(self,msg):
        try:
            Bot(self.token).send_message(chat_id=self.tlg_id,text =msg )
        except:pass
        
    def debug(self,error,extra='',alarm=True):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        inf = datetime.now().strftime("%H:%M") + f" , {fname}:{exc_tb.tb_lineno} => "
        pm =inf 
        try:
            if not isinstance(error,str):
                err= traceback.format_exc()
                errl = err.split('\n')
                err_msg = '\n\t'.join(errl[1:])
                pm+='\n'+err_msg
            else:
                error = str(error)
                pm+='\t'+error
            pm+=f"{extra=}"
            with open(path_maker([],self.relative_path)+'/'+self.log_name,'a+') as f:
                f.write(pm+'\n\n')
                if self.debug_mode:
                    print(pm)
            if self.token and self.tlg_id and alarm and self.alarm_mode:
                log_name =self.log_name
                log_name+='\n'
                self.alarm(f"{log_name=}\n{inf}\n"+str(error)+f"{extra=}")

        except:pass
        return pm
