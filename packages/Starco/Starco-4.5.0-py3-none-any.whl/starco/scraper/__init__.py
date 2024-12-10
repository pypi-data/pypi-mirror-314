
from lxml import etree
from bs4 import BeautifulSoup
import requests


class Scraper:
    def __init__(self, url=None,root:BeautifulSoup=None,html_source:str=None,proxy=None) -> None:
        '''
            proxy = {'https':'http://127.0.0.1:8889'}
        '''
        self.url = url
        self.proxy = proxy
        if url:
            self.root = self.soup()
        elif root:
            self.root =root
        
        elif html_source:
            self.root =BeautifulSoup(html_source, "html.parser")
        
        else:
            raise Exception('root not defind')

    def soup(self):
        try:
            HEADERS = ({'User-Agent':
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                        'Accept-Language': 'en-US, en;q=0.5'})

            webpage = requests.get(self.url, headers=HEADERS,proxies=self.proxy)
            soup = BeautifulSoup(webpage.content, "html.parser")
            
            return soup
        except:print('Error Request To Url')

    def find_all(self, tag, attrs={}):
        '''
            attrs = {'attribut name':'attribut value'}
            ex: find_all( 'div', attrs'= {'class': 'teaser3})
        '''
        return self.root.find_all(tag, attrs)

    def find(self,  tag, attrs={}):
        '''
            attrs = {'attribut name':'attribut value'}
            ex: find_all( 'div', attrs'= {'class': 'teaser3})
        '''
        cfg = {'name':tag,'attrs':attrs}
        return self.root.find(**cfg)

    def xpath(self, xpath:str):
        dom = etree.HTML(str(self.root))
        return dom.xpath(xpath)