# coding=utf-8

import random
import json
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from fake_useragent import UserAgent
from myspider.lib import mongo_helper

class RandomUAMiddleware(UserAgentMiddleware):
    def __init__(self, agents):
        self.agents = agents

    # 从crawler构造，USER_AGENTS定义在crawler的配置的设置中
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    # 从settings构造，USER_AGENTS定义在settings.py中
    @classmethod
    def from_settings(cls, settings):
        return cls(settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        agent = random.choice(self.agents)
        request.headers["User-Agent"] = agent
  
class RandomProxyMiddleware(object):
    def __init__(self):
        self.conn = mongo_helper.Mongo()
        self.proxy = self.conn.proxy.find_one()

    def process_request(self, request, spider):
        http = 'http' if self.proxy['http'] == 'HTTP' else 'https'
        request.meta['proxy'] = '%s://%s' % (http, self.proxy['url'])

class CookieMiddleware(object):
    def __init__(self, cookie):
        self.cookie = {'name': 'andy', 'age': '25'}

    def process_request(self, request, spider):
        request.cookies = json.loads(self.cookie)


class RandomUAMiddleware2(UserAgentMiddleware):
    def __init__(self, crawler):
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
        request.headers.setdefault('User-Agent', get_ua())
