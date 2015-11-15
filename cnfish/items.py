# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnfishItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    crawl_from= scrapy.Field()
    title = scrapy.Field()
    article_info = scrapy.Field()
    article = scrapy.Field()
    imgurl = scrapy.Field()
    tag = scrapy.Field()
