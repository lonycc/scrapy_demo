# coding=utf-8

import scrapy
from scrapy.http import Request,FormRequest
import urllib.request

class douban_login_spider(scrapy.Spider):
    name = 'douban_login'
    allowed_domains = ["douban.com"]

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
        'Connection': 'keep-alive',
        'Host': 'www.douban.com',
        'Upgrade-Insecure-Requests':1
    }

    def start_requests(self):
        return [Request(url='https://accounts.douban.com/login', callback=self.parse, meta={'cookiejar': 1}, dont_filter=True)]

    def parse(self, response):
        captcha = response.xpath('//img[@id="captcha_image"]/@src').extract_first()
        if captcha:
            print('此时有验证码')
            urllib.request.urlretrieve(captcha, filename='captcha.jpg')
            captcha_value = input('请查看本地验证码图片captcha.jpg并输入验证码:')
            captcha_id = response.xpath('//input[@name="captcha-id"]/@value').extract_first()
            data = {
                'form_email': 'mail@domain.com',
                'form_password': 'password',
                'captcha-solution': captcha_value,
                'captcha-id': captcha_id,
                'remember': '',
                'login': ''
            }
        else:
            print('此时没有验证码')
            data = {
                'form_email': 'mail@domain.com',
                'form_password': 'password',
                'remember': '',
                'login': ''
            }
        print('登录中。。。。。。')
        return [FormRequest.from_response(response, meta={'cookiejar': response.meta['cookiejar']}, headers=self.headers, formdata=data, callback=self.next, dont_filter=True)]

    def next(self, response):
        print('此时已经登录完成并爬取了个人中心的数据')
        title = response.xpath('//li[@class="nav-user-account"]/a/span/text()').extract_first()
        print(title)