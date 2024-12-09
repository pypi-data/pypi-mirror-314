# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from gzspidertools.scraper.middlewares.headers.ua import RandomRequestUaMiddleware
from gzspidertools.scraper.middlewares.netlib.aiohttplib import (
    AiohttpDownloaderMiddleware,
)
from gzspidertools.scraper.middlewares.proxy.dynamic import (
    AbuDynamicProxyDownloaderMiddleware,
    DynamicProxyDownloaderMiddleware,
)
from gzspidertools.scraper.middlewares.proxy.exclusive import (
    ExclusiveProxyDownloaderMiddleware,
)

__all__ = [
    "RandomRequestUaMiddleware",
    "AiohttpDownloaderMiddleware",
    "DynamicProxyDownloaderMiddleware",
    "AbuDynamicProxyDownloaderMiddleware",
    "ExclusiveProxyDownloaderMiddleware",
]
