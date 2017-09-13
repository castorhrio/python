import requests
import os
import time
import re
from bs4 import BeautifulSoup
from PIL import Image

cur_path = os.getcwd() + '/zhihu/'

class ZhiHuSpider(object):
    def __init__(self):
        self.session = requests.Session()
        self.url_signin = 'https://www.zhihu.com/#signin'
        self.url_login = 'https://www.zhihu.com/login/email'
        self.url_captcha = 'https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
        self.num = 1

    def get_captcha(self):
        if not os.path.exists(cur_path + 'captcha'):
            os.mkdir(cur_path+'captcha')

        captcha_text = ''
        while True:
            captcha = self.session.get(self.url_captcha,headers=self.headers).content
            captcha_path = cur_path + 'captcha/captcha.png'
            captcha_path_new = cur_path + 'captcha/captcha_new.png'
            with open(captcha_path,'wb') as f:
                f.write(captcha)

            # 图片处理便于识别文字：彩色转灰度，灰度转二值，二值图像识别
            im = Image.open(captcha_path)
            w,h = im.size
            im = im.convert('L')
            threshold = 100
            table = []
            for i in range(256):
                if i < threshold:
                    table.append(0)
                else:
                    table.append(1)
            im = im.point(table,'1')
            w_new,h_new = w*2,h*2
            im = im.resize((w_new,h_new),Image.ANTIALIAS)
            im.save(captcha_path_new)

            captcha_text_path = cur_path + 'captcha/captcha_text'
            cmd = 'tesseract %s %s' %(captcha_path_new,captcha_text_path)
            os.system(cmd)
            time.sleep(3)

            with open('%s.txt' %captcha_text_path,'r') as f:
                try:
                    captcha_text = f.read().strip()
                    print('第 %d 次识别的验证码为：%s' %(self.num,captcha_text))
                    regex = re.compile('^[0-9a-zA-Z]{4}$')
                    if captcha_text and re.search(regex,captcha_text):
                        break;
                    else:
                        print('验证码无效！重新识别中....')
                        self.num += 1
                except Exception as ex:
                    print('get captcha exception:',ex)
                    break
        return captcha_text

    def login(self,username,password):
        soup = BeautifulSoup(self.session.get(self.url_signin,headers=self.headers).content,'html.parser')
        xsrf = soup.find('input',attrs={'name':'_xsrf'}).get('value')
        post_data = {
            '_xsrf':xsrf,
            'email':username,
            'password':password,
            'captcha':self.get_captcha()
        }
        login_ret = self.session.post(self.url_login,post_data,headers=self.headers).json()
        return login_ret

    def parserpage(self):
        try:
            soup = BeautifulSoup(self.session.get(self.url_signin,headers=self.headers).content,'html.parser')
            items = soup.find_all('div',attrs={'class':'Card TopstoryItem'})
            for item in items:
                url = item.find('h2',attrs={'class':'ContentItem-title'}).find('a')['href']
                title = item.find('h2',attrs={'class':'ContentItem-title'}).string
                content = item.find('span',attrs={'class','RichText CopyrightRichText-richText'}).string
                print('title: %s, url: %s, content: %s' %(url,title,content))
        except Exception as ex:
            print('parse page error:' ex)

if __name__ =='__main__':
    zhihu = ZhiHuSpider()
    while True:
        ret = zhihu.login('740415505@qq.com','wasd123...')
        if ret['r'] == 0:
            print('登陆成功！')
            zhihu.parserpage()
            break
        else:
            print('登陆失败:%s' %ret['msg'])

