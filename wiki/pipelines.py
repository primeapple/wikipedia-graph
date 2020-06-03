from scrapy.exceptions import DropItem
from datetime import datetime
import pymongo


################# PIPELINES #################

class CleaningPipeline:
    def process_item(self, item, spider):
        if 'url' in item:
            if not 'title' in item:
                item['title'] = "unknown title"
            if not 'links' in item:
                item['links'] = []
            if not 'categories' in item:
                item['categories'] = []
            return item
        # drop item if we do not have an url
        else:
            raise DropItem("Missing url in %s" % item)


class DatabasePipeline:
    def __init__(self, mongo_uri, mongo_db, collection_name=None):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        if collection_name is None:
            self.collection_name = datetime.now().strftime('date_%Y_%m_%d_%H_%M_%S')
        else:
            self.collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('DATABASE_URI'),
            mongo_db=crawler.settings.get('DATABASE_NAME'),
            collection_name=crawler.spider.collection
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item