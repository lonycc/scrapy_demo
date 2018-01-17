# coding=utf-8

BOT_NAME = 'myspider'

SPIDER_MODULES = ['myspider.spiders']
NEWSPIDER_MODULE = 'myspider.spiders'

ROBOTSTXT_OBEY = False  # 遵守robots协议
LOG_LEVEL = 'DEBUG'  # 日志级别
CONCURRENT_REQUESTS = 20  # 线程数
DOWNLOAD_DELAY = 0.01  # 间隔时间

REDIRECT_ENABLED = True  # 不允许重定向
#HTTPERROR_ALLOWED_CODES = [302, 405, 303, 400,] #允许的http错误状态
COOKIES_ENABLED = False  # 如果启用了cookies, 那么http request会带上cookies; 有些站点会使用cookies发现爬虫轨迹
COOKIES_DEBUG = False  #开启cookies debug

DEPTH_LIMIT = 0 # 不限爬取深度
DEPTH_PRIORITY = 0  # 深度优先级
RETRY_ENABLED= True # 允许重试


DOWNLOADER_MIDDLEWARES = {
    'myspider.middlewares.RandomUAMiddleware': 400,
    #'myspider.middlewares.RandomUAMiddleware2': 401,
    #'myspider.middlewares.RandomProxyMiddleware': 402,
    #'scrapy_proxies.RandomProxy': 100,
    #'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

# 如果使用了scrapy_proxies.RandomProxy
#PROXY_LIST = '/path/to/proxy/list'
#PROXY_MODE = 0
#CUSTOM_PROXY = 'http://host:port'

# 这里的pipeline全局生效, 每个spider通过custom_settings配置pipeline, 会覆盖掉全局的
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300,
}

IMAGES_STORE = 'images'
IMAGES_MIN_HEIGHT = 110 # 图片高度限制
IMAGES_MIN_WIDTH = 110  # 图片宽度限制
IMAGES_EXPIRES = 30 #设置图片失效的时间

# 缩略图
#IMAGES_THUMBS = {
#    'small': (50, 50),
#    'big': (270, 270),
#}


EXTENSIONS = {
    'scrapy.extensions.statsmailer.StatsMailer': 500,
}

#STATSMAILER_RCPTS = ['receiver@domain.com']
MAIL_FROM = 'scrapy@domain.com'
MAIL_HOST = 'smtp.domain.com'
MAIL_PORT = 25
MAIL_USER = 'username'
MAIL_PASS = 'password'
MAIL_TLS = False
MAIL_SSL = False


MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'common'

# 配置url去重规则
DUPEFILTER_CLASS = 'myspider.lib.custom_filters.CustomURLFilter'

USER_AGENTS = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
    'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; Android 7.0; LON-AL00 Build/HUAWEILON-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/4G WebP/0.3.0 Pixel/1440',
    'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-CN; R7Plusm Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.2.942 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.0.2; Redmi Note 2 Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1920',
    'Mozilla/5.0 (Linux; Android 6.0; HUAWEI CRR-UL00 Build/HUAWEICRR-UL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043220 Safari/537.36 MicroMessenger/6.5.7.1041 NetType/4G Language/zh_CN',
    'Mozilla/5.0 (Linux; Android 6.0.1; vivo X9Plus Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/4G WebP/0.3.0 Pixel/1080',
    'Mozilla/5.0 (iPhone 92; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.4.1 Mobile/14F89 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
    'Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; PRO 5 Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.2.942 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.1.1; OPPO A53 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043220 Safari/537.36 MicroMessenger/6.5.8.1060 NetType/4G Language/zh_CN',
    'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MI MAX Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/8.7.8'
]