# -*- coding: utf-8 -*-

# Scrapy settings for pdd_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'pdd_spider'

SPIDER_MODULES = ['pdd_spider.spiders']
NEWSPIDER_MODULE = 'pdd_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pdd_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    # 'pdd_spider.middlewares.PddSpiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'pdd_spider.middlewares.PddSpiderDownloaderMiddleware': 543,
    # 'pdd_spider.middlewares.ProxyMiddleware': 101,
    # 'pdd_spider.middlewares.RandomUserAgentMiddleware': 443,
    # 'pdd_spider.middlewares.RandomCookiesMiddleware': 545,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    # 'pdd_spider.middlewares.TooManyRequestsRetryMiddleware': 540,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'pdd_spider.pipelines.PddSpiderPipeline': 300,
    'pdd_spider.pipelines.MongoPipeline': 300,
    'pdd_spider.pipelines.MysqlPipeline': 301,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# REDIRECT_ENABLED = False
# HTTPERROR_ALLOWED_CODES = [403, 302]
HTTPERROR_ALLOWED_CODES = list(range(300, 600))
# RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408, 429]
RETRY_HTTP_CODES = list(range(400, 600))
RETRY_TIMES = 6


MONGO_URI = 'localhost'
MONGO_DB = 'Pdd_Spider_MongoDB'

MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'pdd_spider'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_PORT = 3306

LOG_LEVEL = 'DEBUG'
LOG_FILE = 'log.txt'
# COMMANDS_MODULE = 'dianping.commands'