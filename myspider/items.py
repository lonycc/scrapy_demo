# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags
import re

# 新闻资讯
class NewsItem(scrapy.Item):
    url = scrapy.Field() # 链接
    author = scrapy.Field() # 作者
    editor = scrapy.Field()  #编辑
    content = scrapy.Field()  # 正文
    title = scrapy.Field() # 标题
    thumbnail = scrapy.Field()  # 缩略图
    pdate = scrapy.Field()  # 发布日期时间
    tag = scrapy.Field()  # 标签
    channel = scrapy.Field()  # 栏目
    description = scrapy.Field() # 摘要
    origin = scrapy.Field() # 新闻源
    website = scrapy.Field() # 网站
    category = scrapy.Field() #类别, 专题/新闻
    has_pic = scrapy.Field()  #是否有图
    has_video = scrapy.Field()  #是否有视频
    reserved_1 = scrapy.Field()  #保留字段1
    reserved_2 = scrapy.Field()  #保留字段2
    reserved_3 = scrapy.Field()  #保留字段3
    reserved_4 = scrapy.Field()  #保留字段4
    reserved_5 = scrapy.Field()  #保留字段5
    reserved_6 = scrapy.Field()  #保留字段6

# 图片
class ImagesItem(scrapy.Item):
    image_urls = scrapy.Field()
    title = scrapy.Field()
    images = scrapy.Field()

# 煎蛋网段子
class JandanDuanItem(scrapy.Item):
    author = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    oo = scrapy.Field()
    xx = scrapy.Field()
    pdate = scrapy.Field()
    uuid = scrapy.Field()

# 煎蛋网自建评论
class JandanCommentItem(scrapy.Item):
    pass

# 代理
class ProxyItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    http = scrapy.Field()
    method = scrapy.Field()
    location = scrapy.Field()
    speed = scrapy.Field()
    url = scrapy.Field()
    anonymous = scrapy.Field()
    verify_time = scrapy.Field()

# 音乐
class MusicItem(scrapy.Item):
    music_name = scrapy.Field()
    music_alias = scrapy.Field()
    music_singer = scrapy.Field()
    music_time = scrapy.Field()
    music_rating = scrapy.Field()
    music_votes = scrapy.Field()
    music_tags = scrapy.Field()
    music_url = scrapy.Field()


# 乐评
class MusicReviewItem(scrapy.Item):
    review_title = scrapy.Field()
    review_content = scrapy.Field()
    review_author = scrapy.Field()
    review_music = scrapy.Field()
    review_time = scrapy.Field()
    review_url = scrapy.Field()


# 视频
class VideoItem(scrapy.Item):
    video_name = scrapy.Field()
    video_alias = scrapy.Field()
    video_actor = scrapy.Field()
    video_year = scrapy.Field()
    video_time = scrapy.Field()
    video_rating = scrapy.Field()
    video_votes = scrapy.Field()
    video_tags = scrapy.Field()
    video_url = scrapy.Field()
    video_director = scrapy.Field()
    video_type = scrapy.Field()
    video_bigtype = scrapy.Field()
    video_area = scrapy.Field()
    video_language = scrapy.Field()
    video_length = scrapy.Field()
    video_writer = scrapy.Field()
    video_desc = scrapy.Field()
    video_episodes = scrapy.Field()


# 影评
class VideoReviewItem(scrapy.Item):
    review_title = scrapy.Field()
    review_content = scrapy.Field()
    review_author = scrapy.Field()
    review_video = scrapy.Field()
    review_time = scrapy.Field()
    review_url = scrapy.Field()

def ends_filter(value):
    #拉勾网清洗函数
    if '查看地图' in value:
        tp_list = value.split('\n')
        v_list = [v.strip() for v in tp_list if '查看地图' not in v]
        return ''.join(v_list).strip()
    elif '发布于拉勾网' in value:
        return value.replace('发布于拉勾网', '').strip()
    elif '/' in value:
        return value.replace('/', '').strip()
    else:
        return value.strip()

class LagouItemLoader(ItemLoader):
    #default_input_processer =
    #default_item_class = scrapy.Item
    default_output_processor = TakeFirst()
    title_in = MapCompose(remove_tags)
    title_out = Join()

class LagouItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    url = scrapy.Field()
    salary = scrapy.Field(input_processor=MapCompose(ends_filter))
    job_city = scrapy.Field(input_processor=MapCompose(ends_filter))
    work_years = scrapy.Field(input_processor=MapCompose(ends_filter))
    degree_need = scrapy.Field(input_processor=MapCompose(ends_filter))
    job_type = scrapy.Field()
    tags = scrapy.Field(output_processor=Join(','))
    publish_time = scrapy.Field(input_processor=MapCompose(ends_filter))
    job_advantage = scrapy.Field(input_processor=Join('\n'))
    job_desc = scrapy.Field(input_processor=Join('\n'))
    work_addr = scrapy.Field(input_processor=MapCompose(remove_tags, ends_filter))
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    crawl_time = scrapy.Field()


def title_filter(value):
    return value.split('_')[0]

def content_filter(value):
    return re.sub(r'\t|\r|\n', '', value)

class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()

class DemoItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags, title_filter),
    )
    content = scrapy.Field(
        input_processor=MapCompose(remove_tags, content_filter),
        output_processor=Join(),
    )

class QiushiItem(scrapy.Item):
    pass