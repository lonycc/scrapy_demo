# coding=utf-8

from myspider.items import JandanDuanItem
from myspider.lib.send_mail import mailSender
from scrapy.http import Request
from scrapy.spiders import CrawlerSpider
from scrapy import signals
from json import loads

class jandan_duan(CrawlSpider):
    name = 'jandan_duan'
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
            'myspider.pipeline.mongo_pipeline.MongoPipeline': 1,
        }
    }

    def start_requests(self):
        yield Request(url='https://i.jandan.net/duan', headers=self.headers, callback=self.parse_duan, errback=self.handle_error, dont_filter=True, meta={'num': 0})

    # 段子
    def parse_duan(self, response):
        num = response.meta['num']
        for duan in response.xpath('//ol[@class="commentlist"]/li[contains(@id, "comment-")]'):
            item = JandanDuanItem()
            item['url'] = duan.xpath('span[@class="righttext"]/a/@href').extract_first()
            id = duan.xpath('span[@class="righttext"]/a/text()').extract_first()
            author = duan.xpath('b')
            item['author'] = author.xpath('string(.)').extract_first()
            item['pdate'] = duan.xpath('span[@class="time"]/text()').extract_first().strip()
            item['content'] = ''.join(duan.xpath('div[@class="commenttext"]/p').extract())
            vote = duan.xpath('div[@class="jandan-vote"]/span[@class="tucao-unlike-container"]/span/text()').extract()
            item['oo'] = vote[0]
            item['xx'] = vote[1]
            comment = duan.xpath('div[@class="jandan-vote"]/a[@class="tucao-btn"]/text()').extract_first()
            yield item
            yield Request(url='https://i.jandan.net/tucao/{0}'.format(id), headers=self.headers, callback=self.parse_comment, meta={'id': id})

        next_url = response.xpath('//a[@class="previous-comment-page"]/@href').extract_first()
        if next_url and num < 30:
            next_url = response.urljoin(next_url)
            num += 1
            yield Request(url=next_url, headers=self.headers, callback=self.parse_duan, meta={'num': num})

    def parse_comment(self, response):
        obj = loads(response.text)
        next_id = 0
        comment_post_id = response.meta['id']
        if obj['code'] == 0:
            for tucao in obj['tucao']:
                tucao['is_hot']  = 0
                next_id = tucao['comment_ID']
                yield tucao
            if len(obj['hot_tucao']) != 0:
                for hot_tucao in obj['hot_tucao']:
                    hot_tucao['is_hot'] = 1
                    yield hot_tucao
            if obj['has_next_page'] == 'true':
                yield Request(url='https://i.jandan.net/tucao/{0}/n/{1}'.format(comment_post_id, next_id), headers=self.headers, callback=self.parse_comment, meta={'id': comment_post_id})

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(jandan_duan, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(spider.spider_error, signal=signals.spider_error)
        return spider

    def spider_closed(self, spider, reason):
        mailsender = mailSender()
        mailsender.send(['receiver@domain.com'], '爬虫 {0} 结束'.format(spider.name), '爬虫结束了, 结束原因 {0}'.format(reason))
        # 下面是用scrapy自带的MailSender, 但当前版本存在问题
        # mailer = MailSender.from_settings(self.settings)
        # return mailer.send(to=['receiver@domain.com'], subject='something error', body='something wrong', cc=['receiver02@domain.com'])

    def spider_error(self, failure, response, spider):
        mailsender = mailSender()
        mailsender.send(['receiver@domain.com'], '爬虫 {0} 错误'.format(spider.name), '爬虫出错了{0}, 结果{1}'.format(failure, response))
    
    def handle_error(self):
        print('something wrong')
        CloseSpider()
