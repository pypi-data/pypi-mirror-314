from scrapy.spiders import CrawlSpider

from gzspidertools.scraper.spiders import AyuSpider

__all__ = [
    "AyuCrawlSpider",
]


class AyuCrawlSpider(AyuSpider, CrawlSpider):  # type: ignore
    def __init__(self, *args, **kwargs):
        AyuSpider.__init__(self, *args, **kwargs)
        CrawlSpider.__init__(self, *args, **kwargs)
