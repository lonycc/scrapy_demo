# coding=utf-8

from myspider.items import QiushiItem
from scrapy.http import Request
from scrapy.spiders import CrawlSpider


class qiushi(CrawlSpider):
    name = 'qiushi'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/8hr/']


    # 糗事百科
    def parse(self, response):
        content_left_div = response.xpath('//div[@id="content-left"]')
        content_div_list = content_left_div.xpath('./div[contains(@id, "qiushi_tag_")]')
        for duan in content_div_list:
            item = QiushiItem()
            user_page = duan.xpath('div[contains(@class, "author")]/a/@href').extract()
            if user_page:
                item['user_page'] = response.urljoin(user_page[0])
            item['user_gravator'] = duan.xpath('div[contains(@class, "author")]/a/img/@src').extract_first()
            item['user_nickname'] = duan.xpath('div[contains(@class, "author")]/a/img/@alt').extract_first()
            item['user_age'] = duan.xpath('div[contains(@class, "author")]/div/text()').extract_first()
            gender = duan.xpath('div[contains(@class, "author")]/div/@class').extract_first()
            if gender:
                item['user_gender'] = gender.split(' ')[1]
            url = duan.xpath('a[@class="contentHerf"]/@href').extract_first()
            item['url'] = response.urljoin(url)
            item['duan_content'] = duan.xpath('a[@class="contentHerf"]/div[@class="content"]').extract_first()
            tu = duan.xpath('div[@class="thumb"]').extract_first()
            if tu:
                item['duan_content'] += tu
            item['duan_pos'] = duan.xpath('div[@class="stats"]/span[@class="stats-vote"]/i[@class="number"]/text()').extract_first()
            yield item
        next_page = content_left_div.xpath('./ul[@class="pagination"]/li[last()]/a/@href').extract()
        if next_page:
            next_url = response.urljoin(next_page[0])
            yield Request(url=next_url, callback=self.parse)
