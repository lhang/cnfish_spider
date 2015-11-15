# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem

class CnfishPipeline(object):

    collection_name = 'CnfishItem'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.crawled = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print '********1********', item['crawl_from'] in self.crawled
        print '########2########', self.db['CnfishItem'].find_one({'crawl_from': item['crawl_from'][0]})
        if item['crawl_from'] in self.crawled or self.db['CnfishItem'].find_one({'crawl_from': item['crawl_from']}):
            DropItem(item)
        else:
            self.crawled.append(item['crawl_from'])
            self.db['CnfishItem'].insert(dict(item))
            return item
