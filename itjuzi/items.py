# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItjuziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    com_scope = scrapy.Field()
    round = scrapy.Field()
    money = scrapy.Field()
    investor = scrapy.Field()
    valuation = scrapy.Field()
    prov = scrapy.Field()
    agg_time = scrapy.Field()
    com_registered_name = scrapy.Field()



