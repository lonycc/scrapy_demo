# coding=utf-8

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from myspider.items import NewsItem

class demo(CrawlSpider):
    name = 'demo'
    custom_settings = {
        'ITEM_PIPELINES': {
            'myspider.pipeline.json_pipeline.DefaultPipeline': 1,
        }
    }
    allowed_domains = ['jyc.kxue.com']

    def start_requests(self):
        yield Request(url='http://jyc.kxue.com/', callback=self.parse_list)

    def parse_list(self, response):
        letter_li = response.xpath('//ul[@class="index"]/li/a/@href').extract()
        for letter in letter_li:
            yield Request(url=response.urljoin(letter), callback=self.parse_detail)

    def parse_detail(self, response):
        licontent = response.xpath('//div[contains(@class, "jyclist")]/li[@class="licontent"]')
        for li in licontent:
            item = NewsItem()
            item['url'] = li.xpath('./span[@class="hz"]/a/text()').extract_first()
            item['title'] = li.xpath('./span[@class="hz"]/span[@class="js"]/text()').extract_first()
            yield item

        next_page = response.xpath('//ul[@class="pagelist"]/a[text()="下一页"]/@href').extract_first()
        if next_page:
            yield Request(url=resopnse.urljoin(next_page), callback=self.parse_detail)

        next_letter = response.xpath('//div[@class="letters"]/a/@href').extract()
        for  next_letter_url in next_letter:
            yield Request(url=response.urljoin(next_letter_url), callback=self.parse_detail)



