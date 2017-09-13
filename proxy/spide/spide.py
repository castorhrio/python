import requests
from lxml import etree
import time
from bs4 import BeautifulSoup

class Proxy(object):
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
        self.url = None
        self.proxy = None

    def get_data(self):
        data_list = []
        content = self.session.get(self.url,headers=self.headers).content
        if '66' in self.url:
            data_ip = etree.HTML(content).xpath('//*[@id="main"]/div/div[1]/table/tr[position()>1]/td[1]/text()')
            data_port = etree.HTML(content).xpath('//*[@id="main"]/div/div[1]/table/tr[position()>1]/td[2]/text()')
            data_time = etree.HTML(content).xpath('//*[@id="main"]/div/div[1]/table/tr[position()>1]/td[5]/text()')
            data_addr = etree.HTML(content).xpath('//*[@id="main"]/div/div[1]/table/tr[position()>1]/td[3]/text()')        
        
        for i in range(0,len(data_ip)):
            datas = []
            datas.append(data_ip[i])
            datas.append(data_port[i])
            datas.append(data_time[i])
            datas.append(data_addr[i])
            data_list.append(datas)
        
        return data_list
        # with open('data.txt','a') as fd:
        #     for i in range(0,len(data_ip)):
        #         out = u""
        #         out += u"" +data_ip[i]
        #         out += u" : " + data_port[i]
        #         out += u" : " + data_addr[i]
        #         out += u" : " + data_time[i]
        #         fd.write(out + u"\n")

    def get_count(self):
        soup = BeautifulSoup(self.session.get(self.url,headers=self.headers).content,'html.parser')
        if '66' in self.url:
            pagecount = soup.find('div',id='PageList').find('a',class_='dotdot').next_sibling.next_sibling.string
            return pagecount
    
    def verif_ip(self):
        result = False
        test_url = 'https://www.baidu.com/'
        code = self.session.get(test_url,headers=self.headers,proxies=self.proxy).status_code
        if code == 200:
            result = True
        return result