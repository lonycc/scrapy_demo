# coding=utf-8

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from myspider.items import LagouItemLoader, LagouItem
from scrapy.mail import MailSender
from scrapy.conf import settings
import datetime


class lagou(CrawlSpider):
    mailer = MailSender.from_settings(settings)
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']
    rules = (
        Rule(LinkExtractor(allow=(r'zhaopin/.*',)), follow=True),
        Rule(LinkExtractor(allow=(r'gongsi/j\d\.html',)), follow=True),
        Rule(LinkExtractor(allow=(r'jobs/.*',),
        restrict_css=("div#s_position_list ul.item_con_list"),),
        callback='parse_item', follow=False),
    )

    # LinkExtractor
    # 作用：response对象中获取链接，并且该链接会被接下来爬取
    # 使用：通过SmglLinkExtractor提取希望获取的链接
    # 主要参数：
    # allow：满足括号中“正则表达式”的值会被提取，如果为空，则全部匹配;
    # 并跟进链接(没有callback意味着follow默认为True)
    # deny：与这个正则表达式(或正则表达式列表)
    # 不匹配的URL一定不提取
    # allow_domains：会被提取的链接的domains
    # deny_domains：一定不会被提取链接的domains
    # restrict_xpaths：使用xpath表达式，和allow共同作用过滤链接
    # 当编写爬虫规则时，请避免使用parse作为回调函数
    # CrawlSpider使用parse方法来实现其逻辑，如果您覆盖了parse方法，crawlspider将会运行失败

    def parse_item(self, response):
        Item_loader = LagouItemLoader(item=LagouItem(), response=response)
        #在scrapy shell调试需要.extract()方法,而item_loader则不需要.extract()方法
        Item_loader.add_css('title', 'div.job-name::attr(title)')
        Item_loader.add_value('url', response.url)
        Item_loader.add_css('salary', 'span.salary::text')
        Item_loader.add_xpath('job_city', './/*[@class ="job_request"]/p/span[2]/text()')
        Item_loader.add_xpath('work_years', './/*[@class="job_request"]/p/span[3]/text()')
        Item_loader.add_xpath('degree_need', './/*[@class="job_request"]/p/span[4]/text()')
        Item_loader.add_xpath('job_type', './/*[@class ="job_request"]/p/span[5]/text()')
        Item_loader.add_css('tags', 'li.labels::text')
        Item_loader.add_css('publish_time', 'p.publish_time::text')
        Item_loader.add_css('job_advantage', 'dd.job-advantage p::text')
        Item_loader.add_css('job_desc', 'dd.job_bt div p::text')
        Item_loader.add_css('work_addr', 'div.work_addr')
        Item_loader.add_css('company_name', 'dl.job_company a img::attr(alt)')
        Item_loader.add_css('company_url', 'dl.job_company dt a::attr(href)')
        Item_loader.add_value('crawl_time', datetime.datetime.now())
        # itemloader只用来编写抓取逻辑，数据清洗放在items中进行
        lagou_item_loader = Item_loader.load_item()
        return lagou_item_loader