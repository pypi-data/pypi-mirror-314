from setuptools import setup,find_packages
import os,glob
requires = [
    'cffi',
    'cryptography',
    'pycparser==2.21',
    'beautifulsoup4==4.12.2',
    'lxml==4.9.3',
    'requests',
    'easy-db==0.9.15',
    'hcloud==1.32.0',
    'cloudflare==2.11.6',
    'python-socks==2.4.3',
    'python-telegram-bot==13.14',
    'Telethon==1.33.1',
    'phonenumbers',
    'pycountry',
    'nest-asyncio==1.5.8',
    'zibal',
    'nowpayments',
    'jdatetime',
    'deep-translator',
    'async-timeout',
    'PySocks',
    'selenium==4.17.2',
    'pyperclip==1.8.2',
    'pandas',
    'starco-utility'
    
]

setup(
    name = 'Starco',long_description='starco project',
    version='5.0.1',
    author='Mojtaba Tahmasbi',
    packages=find_packages(),
    install_requires=requires,
)
