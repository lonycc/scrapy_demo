# coding=utf-8

from scrapy.http import Request, FormRequest
import scrapy
from urllib.parse import quote_plus
import base64
import rsa
import requests
import re
import time
import binascii
from PIL import Image
import random

class WeiboLoginSpider(scrapy.Spider):
    name = 'weibo_login'
    session = requests.session()
    headers = {}

    def start_requests(self):
        return [Request(url='http://weibo.com/login.php', meta={'cookiejar': 1}, callback=self.get_su)]

    def get_su(self, response):
        username = input('请输入用户名:')
        username_quote = quote_plus(username)
        username_base64 = base64.b64encode(username_quote.encode('utf-8')).decode('utf-8')
        meta = {'cookiejar': response.meta['cookiejar'], 'username_base64': username_base64}
        pre_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su={username}&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_={time}'.format(username=username_base64, time=int(time.time() * 1000))
        return [Request(pre_url, meta=meta, callback=self.server_data)]

    def server_data(self, response):
        server_data = eval(response.body.decode('utf-8').replace("sinaSSOController.preloginCallBack", ''))
        print(server_data)
        meta =response.meta
        meta['server_data'] = server_data
        return [Request('https://baidu.com', meta=meta, callback=self.get_password)]

    def get_password(self, response):
        password = input('请输入密码:')
        servertime = response.meta['server_data']['servertime']
        nonce = response.meta['server_data']['nonce']
        pubkey = response.meta['server_data']['pubkey']
        rsapublickey = int(pubkey, 16)   #转话为10进制
        key = rsa.PublicKey(rsapublickey, 65537)
        message = '{0}\t{1}\n{2}'.format(servertime, nonce, password)
        message = message.encode('utf-8')
        passwd = rsa.encrypt(message, key)
        passwd = binascii.b2a_hex(passwd)
        print(passwd)
        meta = response.meta
        meta['passwd'] = passwd
        return [Request('http://www.sina.com.cn/', meta=meta, callback=self.login)]

    def login(self, response):
        su = response.meta['username_base64']
        servertime = response.meta['server_data']['servertime']
        nonce = response.meta['server_data']['nonce']
        rsakv = response.meta['server_data']['rsakv']
        password_secret = response.meta['passwd']
        postdata = {
            'entry':'weibo',
            'gateway':'1',
            'from':'',
            'savestate':'7',
            'useticket':'1',
            'pagerefer':"http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
            'wsseretry':'servertime_error',
            'vsnf':'1',
            'su':su,
            'service':'miniblog',
            'servertime':str(servertime),
            'nonce':nonce,
            'pwencode':'rsa2',
            'rsakv':rsakv,
            'sp':password_secret,
            'sr':'1536*864',
            'encoding':'UTF-8',
            'prelt':'105',
            'url':'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype':'META'
        }
        login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        print(postdata)
        if response.meta['server_data']['showpin'] == 0:
            return [FormRequest(login_url, meta={'cookiejar': response.meta['cookiejar']}, formdata=postdata, callback=self.get_loop_url, dont_filter=True)]
        else:   #获得验证码, 手动输入
            cha_url = 'http://login.sina.com.cn/cgi/pin.php?r={0}&s=0&p={1}'.format(int(random.random() * 100000000), response.meta['server_data']['picd'])
            cha_page = self.session.get(cha_url, cookies=response.meta['cookiejar'], headers=self.headers)
            with open("cha.jpg", 'wb') as f:
                f.write(cha_page.content)
                f.close()
            try:
                im = Image.open("cha.jpg")
                im.show()
                im.close()
            except:
                print("请到当前目录下，找到验证码后输入")

    def get_loop_url(self, response):
        login_loop = response.body.decode('gbk')
        pa = r'location\.replace\([\'"](.*?)[\'"]\)'
        loop_url = re.findall(pa, login_loop)[0]
        print(loop_url)
        return [Request(loop_url, meta={'cookiejar':response.meta['cookiejar']}, callback=self.after_login)]

    def after_login(self,response):
        return [Request('http://weibo.com/', meta={'cookiejar':response.meta['cookiejar']}, callback=self.parse)]

    def parse(self, response):
        print(response.body)
