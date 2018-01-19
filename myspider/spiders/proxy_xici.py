# coding=utf-8

from scrapy.http import Request
import scrapy
from myspider.items import ProxyItem

class xicidaili(scrapy.Spider):
    name = 'proxy_xici'
    allowed_domains = ['www.xicidaili.com']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-Cn,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.xicidaili.com',
        'Origin': 'http://evil.com/'
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'myspider.pipeline.mongo_pipeline.MongoPipeline': 1,
        }
    }

    def start_requests(self):
        url_list = ['http://www.xicidaili.com/nn/%d' % i for i in range(1, 11)]
        for url in url_list:
            yield Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        for tr in response.xpath('//table[@id="ip_list"]/tr[@class=""] | //table[@id="ip_list"]/tr[@class="odd"]'):
            item = ProxyItem()
            td = tr.xpath('td')

            item['ip'] = td[1].xpath('string(.)').extract_first()
            item['port'] = td[2].xpath('string(.)').extract_first()
            item['anonymous'] = td[4].xpath('string(.)').extract_first()
            item['http'] = td[5].xpath('string(.)').extract_first()
            item['method'] = ''
            item['location'] = td[3].xpath('a/text()').extract_first()
            item['speed'] = td[6].xpath('div/@title').extract_first()
            item['url'] = '%s:%s' % (item['ip'], item['port'])
            item['verify_time'] = td[9].xpath('string(.)').extract_first()
            yield item
