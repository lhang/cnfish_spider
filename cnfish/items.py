# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnfishItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    imgurl = scrapy.Field()
    img = scrapy.Field()
    article = scrapy.Field()
    tag1 = scrapy.Field()
    tag2 = scrapy.Field()
