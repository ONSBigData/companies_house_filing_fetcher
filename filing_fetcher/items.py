# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FilingItem(scrapy.Item):
    pages = scrapy.Field()
    date = scrapy.Field()
    type = scrapy.Field()
    barcode = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    company_number = scrapy.Field()
    made_up_date = scrapy.Field()
