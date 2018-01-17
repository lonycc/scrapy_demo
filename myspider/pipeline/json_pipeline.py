# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from datetime import datetime

class JsonPipeline(object):
    def open_spider(self, spider):
        self.file = codecs.open('{0}_{1}.json'.format(spider.name, datetime.now().strftime('%Y%m%d')), 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False)
        self.file.write('{0}\n'.format(line))
        return item

    def close_spider(self, spider):
        self.file.close()
        print('{0} closed'.format(spider.name))

class DefaultPipeline(object):
    def process_item(self, item, spider):
        return item
