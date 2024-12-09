from twisted.internet import defer, reactor

from gzspidertools.common.mongodbpipe import TwistedAsynchronous, mongodb_pipe
from gzspidertools.common.multiplexing import ReuseOperation
from gzspidertools.scraper.pipelines.mongo.fantasy import AyuFtyMongoPipeline

__all__ = [
    "AyuTwistedMongoPipeline",
]


class AyuTwistedMongoPipeline(AyuFtyMongoPipeline):
    @defer.inlineCallbacks
    def process_item(self, item, spider):
        out = defer.Deferred()
        reactor.callInThread(self.db_insert, item, out)
        yield out
        defer.returnValue(item)

    def db_insert(self, item, out):
        item_dict = ReuseOperation.item_to_dict(item)
        mongodb_pipe(TwistedAsynchronous(), item_dict=item_dict, db=self.db)
        reactor.callFromThread(out.callback, item_dict)
