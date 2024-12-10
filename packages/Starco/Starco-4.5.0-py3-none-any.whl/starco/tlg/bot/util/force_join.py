from starco.utils import get_timestamp
def force_check_get_status_db(self,uid):
    try:
        if uid:
            user_item=self.db.do("users",condition=f"id={uid}")[0]
            force_check_ts=user_item['force_check_ts']
            force_check_staus=user_item['force_check_staus']
            if get_timestamp('now') - force_check_ts<5000:
                return force_check_staus
    except Exception as e:print(e)

def force_check_set_status_db(self,status,uid):
    if uid:
        self.db.do("users",{'force_check_ts':get_timestamp('now'),'force_check_staus':status},condition=f"id={uid}")
    
   