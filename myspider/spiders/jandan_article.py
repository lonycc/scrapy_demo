# coding=utf-8

from myspider.items import NewsItem
from scrapy.http import Request
import scrapy
import re

class jandan_article(scrapy.Spider):
    name = 'jandan_article'
    allowed_domains = ['jandan.net']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-Cn,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'jandan.net'
    }
    custom_settings = {
        'ITEM_PIPELINES': {
            'myspider.pipeline.mongo_pipeline.MongoPipeline': 1,
        }
    }

    def start_requests(self):
        yield Request(url='https://jandan.net', headers=self.headers, callback=self.parse)

    def parse(self, response):
        sel = scrapy.Selector(response)
        links_in_a_page = sel.xpath("//a[@href]")
        for link_sel in links_in_a_page:
            link = str(link_sel.re('href="(.*?)"')[0])
            link = response.urljoin(link)
            if re.match(r'https://jandan.net/page/\d{1,4}$', link):
                yield Request(url=link, headers=self.headers, callback=self.parse)
            elif re.match(r'https://jandan.net/20\d{2}/(0[1-9]|1[0-2])/(0[1-9]|[1-2][0-9]|3[0-1])/(.*?).html$', link):
                yield Request(url=link, headers=self.headers, callback=self.parse_detail)

    def parse_detail(self, response):
        item = NewsItem()
        item['url'] = response.url
        item['title'] = response.xpath("//title/text()").extract_first().replace('\r\n', '')
        item['author'] = response.xpath("//a[@class='post-author']/text()").extract_first()
        item['content'] = "". join(response.xpath("//div[@class='post f']//p | //div[@class='post f']/h4").extract())
        item['pic'] = response.xpath("//div[@id='content']//img/@data-original").extract_first()
        item['pdate'] = response.xpath("//div[@class='time_s']/text()").extract_first().replace('@ ', '').replace(' , ', ' ')
        yield item
