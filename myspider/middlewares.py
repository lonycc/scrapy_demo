# coding=utf-8

import random
import json
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from fake_useragent import UserAgent

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