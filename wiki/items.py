# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Identity

################# ITEMS #################
class WikipageItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    links = scrapy.Field()
    categories = scrapy.Field()

################# LOADERS #################
class WikipageLoader(scrapy.loader.ItemLoader):
    default_output_processor = TakeFirst()
    links_out = Identity()
    categories_out = Identity()