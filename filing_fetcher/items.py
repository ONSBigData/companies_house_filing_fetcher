# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FilingItem(scrapy.Item):
    # From the BasicCompanyInformation file
    company_number = scrapy.Field()
    company_status = scrapy.Field()
    incorporation_date = scrapy.Field()
    accounts_next_due_date = scrapy.Field()
    accounts_last_made_up_date = scrapy.Field()
    accounts_account_category = scrapy.Field()

    # From the filing-history
    pages = scrapy.Field()
    date = scrapy.Field()
    type = scrapy.Field()
    barcode = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    made_up_date = scrapy.Field()
    filing_history_status = scrapy.Field()
