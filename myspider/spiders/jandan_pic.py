# coding=utf-8

from myspider.items import ImagesItem
from scrapy.http import Request
import scrapy
import re

class JandanPicSpider(scrapy.Spider):
    name = 'jandan_pic'
    allowed_domains = ['i.jandan.net']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-Cn,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'i.jandan.net'
    }
    custom_settings = {
        'ITEM_PIPELINES': {
            'myspider.pipeline.images_pipeline.MyImagesPipeline': 1,
        }
    }

    def start_requests(self):
        yield Request(url='https://i.jandan.net/pic', headers=self.headers, callback=self.parse)
        yield Request(url='https://i.jandan.net/ooxx', headers=self.headers, callback=self.parse)
        yield Request(url='https://i.jandan.net/drawings', headers=self.headers, callback=self.parse)

    def parse(self, response):
        item = ImagesItem()
        imgs = response.xpath('//ol[@class="commentlist"]//li/div[@class="commenttext"]//img/@src').extract()
        item['image_urls'] = ['https:' + img for img in imgs]
        item['title'] = response.url.split('/')[-1] if 'page-' not in response.url else response.url.split('/')[-2]
        yield item

        next_url = response.xpath('//a[@class="previous-comment-page"]/@href').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield Request(url=next_url, headers=self.headers, callback=self.parse)
