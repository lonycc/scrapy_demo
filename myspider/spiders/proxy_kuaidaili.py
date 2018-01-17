# coding=utf-8

from scrapy.http import Request
import scrapy
from myspider.items import ProxyItem

class KuaiSpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['www.kuaidaili.com']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-Cn,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.kuaidaili.com'
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'myspider.pipeline.mongo_pipeline.MongoPipeline': 1,
        }
    }

    def start_requests(self):
        url_list = ['http://www.kuaidaili.com/proxylist/%d/' % i for i in range(1, 11)]
        for url in url_list:
            yield Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        for tr in response.xpath('//table/tbody/tr'):
            item = ProxyItem()
            item['ip'] = tr.xpath('td[@data-title="IP"]/text()').extract_first()
            item['port'] = tr.xpath('td[@data-title="PORT"]/text()').extract_first()
            item['anonymous'] = tr.xpath('td[@data-title="匿名度"]/text()').extract_first()
            item['http'] = tr.xpath('td[@data-title="类型"]/text()').extract_first()
            item['method'] = tr.xpath('td[@data-title="get/post支持"]/text()').extract_first()
            item['location'] = tr.xpath('td[@data-title="位置"]/text()').extract_first()
            item['speed'] = tr.xpath('td[@data-title="响应速度"]/text()').extract_first()
            item['url'] = '%s:%s' % (item['ip'], item['port'])
            yield item