# coding=utf-8

from scrapy.http import FormRequest, Request
import scrapy

class ZhihuLoginSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/',
        'Upgrade-Insecure-Requests': '1'
    }

    def start_requests(self):
        yield Request(url='https://www.zhihu.com/#signin', meta={'cookiejar' : 1}, headers=self.headers, callback=self.post_login)

    def post_login(self, response):
        _xsrf = response.xpath('//form/input[@name="_xsrf"]/@value').extract_first()
        captcha_type = 'cn'
        account = ''
        password = ''
        captcha = '2'

        formdata = {'_xsrf': _xsrf, 'captcha': captcha, 'captcha_type': captcha_type, 'account': account, 'password': password}

        yield FormRequest.from_response(response, meta={'cookiejar': response.meta['cookiejar']}, formdata=formdata, callback=self.after_login)

    def after_login(self, response):
        print(response.body)
