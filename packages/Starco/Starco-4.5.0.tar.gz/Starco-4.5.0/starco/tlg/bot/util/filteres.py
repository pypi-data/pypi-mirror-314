from telegram.ext.filters import MessageFilter,UpdateFilter,BaseFilter
from.enum import Role
from telegram import Update
from telegram.ext import Filters

from .enum import CONFIRMED


class match_text(MessageFilter):
    def __init__(self, target) -> None:
        super(match_text, self).__init__()
        self.target = target

    def filter(self, message):
        return self.target == message.text

class IsReplied(MessageFilter):
    def __init__(self,*args) -> None:
        super(IsReplied, self).__init__()
    def filter(self, message):
        out = message.reply_to_message!=None and message.chat.id==message.reply_to_message.chat.id
        return out

class special_user(MessageFilter):
    def __init__(self, target) -> None:
        super(special_user, self).__init__()
        self.target = target

    def filter(self, message):
        return self.target == message.from_user.id
    
class match_btn(MessageFilter):
    def __init__(self, target,super_self) -> None:
        super(match_btn, self).__init__()
        self.target = target
        self.super_self = super_self

    def filter(self, message):
        res = self.super_self.replace_btn_label(self.target, main_word= message.text) == message.text
        return res

class RoleFilter(UpdateFilter):
    """Represents a filter that has been inverted.

    Args:
        f: The filter to invert.

    """

    __slots__ = ('f',)

    def __init__(self, f,*args):
        self.f = f

    def filter(self, update) -> bool:
        if not update.message:return False
        try:
            super_self = self.f
            u_id = update.message.from_user.id
            user = super_self.db.do('users',condition=f"id={u_id}")
            if user:
                res = user[0]['role'] == super_self.role
                return res
            if u_id in super_self.superAdmins:
                return True
            return Role.USER.value == super_self.role
        except Exception as e:
            super_self.log(e)
        return True
 
class FileFormat(UpdateFilter):
    """Represents a filter that has been inverted.

    Args:
        f: The filter to invert.

    """

    __slots__ = ('format')

    def __init__(self, format:str,*args):
        self.format:str = format

    def filter(self, update:Update) -> bool:
        try:
            format = self.format.lower()
            file_path =update.effective_message.effective_attachment
            if file_path:
                file_path=file_path.get_file().file_path
                file_format = file_path.split('.')[-1].lower()
                if format==file_format:
                    return True
        except Exception as e:print(e)
        return False
from .force_join import * 
class ForceJoinFilter(UpdateFilter):
    __slots__ = ('super_self')
    def __init__(self, super_self:str,*args):
        self.super_self = super_self

    def filter(self, update:Update) -> bool:
        try:
            status=True
            super_self = self.super_self
            uid =update.message.from_user.id
            fcdb= force_check_get_status_db(super_self,uid)
            print(f"{fcdb=}")
            if fcdb:return True
            channels = super_self.db.do('force_join',condition=f"status={CONFIRMED}")
            print('check FJ')
            if len(channels) > 0:
                for ch in channels:
                    channel_id = ch['channel_id']
                    try:
                        if not super_self.context.bot.getChatMember(channel_id, uid)['status'] in ['member', 'administrator', 'creator']:
                            status= False
                            break
                    except Exception as e:
                        print(2,e)
        except Exception as e:print(1,e)
        print('joind ok')
        force_check_set_status_db(super_self,status,uid)
        return status

class SelectLanguageFilter(UpdateFilter):
    __slots__ = ('super_self')
    def __init__(self, super_self:str,*args):
        self.super_self = super_self

    def filter(self, update:Update) -> bool:
        try:
            ulanguage = self.super_self.user('language')
            uid = update.message.from_user.id
            if ulanguage==None:
                self.super_self.user_info=self.super_self.get_user_info_from_db([],uid)
                ulanguage = self.super_self.user('language')
            languages = self.super_self.languages
            if  ulanguage in [self.super_self.defulat_lang_code,None] and languages:
                return True
        except Exception as e:print(1,e)
        return False

class SharePhoneFilter(UpdateFilter):
    __slots__ = ('super_self')
    def __init__(self, super_self:str,*args):
        self.super_self = super_self

    def filter(self, update:Update) -> bool:
        try:
            phone = self.super_self.user('phone')
            if  phone in [0,None] and not Filters.contact(update):
                return True
        except Exception as e:print(1,e)
        return False