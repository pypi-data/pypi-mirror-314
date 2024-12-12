# Define your item pipelines here
#
# Don"t forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from gzspidertools.scraper.pipelines.download.file import FilesDownloadPipeline
from gzspidertools.scraper.pipelines.es.asynced import AyuAsyncESPipeline
from gzspidertools.scraper.pipelines.es.fantasy import AyuFtyESPipeline
from gzspidertools.scraper.pipelines.mongo.asynced import AyuAsyncMongoPipeline
from gzspidertools.scraper.pipelines.mongo.fantasy import AyuFtyMongoPipeline
from gzspidertools.scraper.pipelines.mongo.twisted import AyuTwistedMongoPipeline
from gzspidertools.scraper.pipelines.msgproducer.mqpub import AyuMQPipeline
from gzspidertools.scraper.pipelines.mysql import AyuMysqlPipeline
from gzspidertools.scraper.pipelines.mysql.asynced import AyuAsyncMysqlPipeline
from gzspidertools.scraper.pipelines.mysql.fantasy import AyuFtyMysqlPipeline
from gzspidertools.scraper.pipelines.mysql.stats import AyuStatisticsMysqlPipeline
from gzspidertools.scraper.pipelines.mysql.turbo import AyuTurboMysqlPipeline
from gzspidertools.scraper.pipelines.mysql.twisted import AyuTwistedMysqlPipeline
from gzspidertools.scraper.pipelines.oracle.fantasy import AyuFtyOraclePipeline
from gzspidertools.scraper.pipelines.oracle.twisted import AyuTwistedOraclePipeline
from gzspidertools.scraper.pipelines.oss.ali import AyuAsyncOssPipeline
from gzspidertools.scraper.pipelines.postgres.asynced import AyuAsyncPostgresPipeline
from gzspidertools.scraper.pipelines.postgres.fantasy import AyuFtyPostgresPipeline
from gzspidertools.scraper.pipelines.postgres.twisted import (
    AyuTwistedPostgresPipeline,
)

__all__ = [
    "FilesDownloadPipeline",
    "AyuFtyESPipeline",
    "AyuAsyncESPipeline",
    "AyuAsyncMongoPipeline",
    "AyuFtyMongoPipeline",
    "AyuTwistedMongoPipeline",
    "AyuMQPipeline",
    "AyuMysqlPipeline",
    "AyuAsyncMysqlPipeline",
    "AyuFtyMysqlPipeline",
    "AyuStatisticsMysqlPipeline",
    "AyuTurboMysqlPipeline",
    "AyuTwistedMysqlPipeline",
    "AyuFtyOraclePipeline",
    "AyuTwistedOraclePipeline",
    "AyuAsyncOssPipeline",
    "AyuAsyncPostgresPipeline",
    "AyuFtyPostgresPipeline",
    "AyuTwistedPostgresPipeline",
]
