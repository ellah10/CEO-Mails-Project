# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field, Item
import scrapy.item


class CeoemailsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company = scrapy.Field()
    ceo_name = scrapy.Field()
    email = scrapy.Field()
    country = scrapy.Field()
    