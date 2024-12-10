from enum import Enum

# class syntax
class Role(Enum):
    ADMIN = 1
    USER = 2
    ACCOUNTER= 3
    ROLE_A=4
    ROLE_B=5
    ROLE_C=6


class ConversationNode():
    entries=[]
    states={}
    fallbacks=[]
    arges = {}

class Node:
    command=None
    command_filters=None
    filters=None
    pattern=None
    callback=None
    btn=None
    msg=None
    chat_id=0
    send_args={}
    args={}
    state_idx=None

class Pack:
    name:str
    entry:list[Node]
    states:list[Node]=None
    fallbacks:list[Node]=None
    db_config:dict[dict]={}
    kargs={}
    
class HeadPack:
    name:str
    func=None
    db_config:dict[dict]={}
    pack:Pack=None
    
   

DEPOSIT = 1
WITHDRAW=2
ADMIN_CHARGE=3
ORDER_PRODUCT=4
EXPENS1=5
EXPENS2=6
EXPENS3=7
EXPENS4=8

WAITING=0
CONFIRMED=1
REJECTED=2
REQUESTED=3

BTN_PFX='_btn'

