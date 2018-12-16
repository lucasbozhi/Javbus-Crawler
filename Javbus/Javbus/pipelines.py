# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class MongoDBPipeline(object):

    def __init__(self):
        host = settings['MONGODB_SERVER']
        port = settings['MONGODB_PORT']
        connection = pymongo.MongoClient(host,port)
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {}!".format(data))
        if valid:
            self.collection.update({"url":item["url"]},dict(item),True,True)
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item


class JavbusPipeline(object):
    def process_item(self, item, spider):
        return item
