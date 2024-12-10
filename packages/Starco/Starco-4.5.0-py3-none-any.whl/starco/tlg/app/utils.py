import re,json
from starco.utils import path_maker
CFG = {
        'api_id':17203958,
        'api_hash':'82cefc4001e057c9d1488ab90e23d54f',
        'device_model':'Telegram Desktop 4.12.2',
        'system_version':'5.15.1',
        'app_version':'1.6.7',
        'number':None,
        'session':None,
        'lang_code':'en',
        'system_lang_code':'en',
        'proxy':None,
        'password_2fa':None,
    }

def get_number(txt):
    txt = str(txt)
    numbers =re.findall(r'\d+', txt)
    if numbers:
        sn = ''.join(numbers)
        sn = sn.lstrip('0')
        return int(sn)


import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_country_code
from phonenumbers.phonenumberutil import region_code_for_number
import pycountry

def get_country_name(phone_number):
    try:
        phone_number = str(phone_number)
        if phone_number[0]!='+':phone_number=f"+{phone_number}"
        pn = phonenumbers.parse(phone_number)
        country = pycountry.countries.get(alpha_2=region_code_for_number(pn)).name
        country = country.replace(' ','_').replace(',','')
        return country
    except:return 'other'

def account_path_list(number, dtype='json', add_country=False):
    number = str(number)
    number = number.replace('+', '')
    out = ['accounts', dtype]
    if add_country:
        out += [get_country_name(number)]
    out += [number]
    return out

def path_for_tlg(number, dtype='json', add_country=False):
    number = clean_number(number)
    pl = account_path_list(number, dtype=dtype, add_country=add_country)
    number = pl[-1]
    return path_maker(pl)+f'/{number}.{dtype}'

def cfg_from_json(number,json_path=None):
    number= clean_number(number)
    if not json_path:
        json_path=path_for_tlg(number)
    try:
        with open(json_path, 'r') as f:
            cfg = json.loads(f.read())
    except:cfg={'number':number}
    return ready_cfg(**cfg)

def clean_number(number):
    number=str(number)
    number = number.replace('+', '')
    return number

def ready_cfg(number: str, **data):
    number = clean_number(number)
    cfg=CFG.copy()
    cfg['number']= number
    cfg['session']= path_for_tlg(number,data.get('dtype','session'))
    for i in cfg:
        if val:=data.get(i):
            cfg[i]=val
    return cfg

def save_json(tlg, json_path: str, p2fa=None):
    init_request = tlg._init_request
    device_model = init_request.device_model
    system_version = init_request.system_version
    app_version = init_request.app_version
    system_lang_code = init_request.system_lang_code
    lang_code = init_request.lang_code
    cfg=CFG.copy()
    cfg['api_id'] = tlg.api_id
    cfg['number'] = tlg.number
    cfg['api_hash'] = tlg.api_hash
    cfg['device_model'] = device_model
    cfg['system_version'] = system_version
    cfg['app_version'] = app_version
    cfg['system_lang_code'] = system_lang_code
    cfg['lang_code'] = lang_code
    cfg['password_2fa'] = p2fa

    with open(json_path, 'w') as f:
        f.write(json.dumps(cfg))





