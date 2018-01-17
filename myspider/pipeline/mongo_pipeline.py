# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from myspider.items import NewsItem

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    def open_spider(self, spider):
        self.conn = pymongo.MongoClient(self.mongo_uri)
        self.db = self.conn[self.mongo_db] # 数据库
        #self.db.authenticate('user', 'passwd')  #帐号认证

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE', 'common')
        )

    def process_item(self, item, spider):
        if isinstance(item, NewsItem):
            collection = self.db['search']
            connection_suggest = self.db_suggest['news']
            collection.update({'url': item['url']}, dict(item), True)
        else:
            collection = self.db[spider.name]
            collection.update({'url': item['url']}, dict(item), True)
        return item

    def close_spider(self, spider):
        self.conn.close()