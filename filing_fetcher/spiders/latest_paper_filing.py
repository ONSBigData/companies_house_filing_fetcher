# -*- coding: utf-8 -*-
import scrapy


class LatestPaperFilingSpider(scrapy.Spider):
    name = 'latest_paper_filing'
    allowed_domains = ['api.companieshouse.gov.uk']
    start_urls = ['http://api.companieshouse.gov.uk/']

    def parse(self, response):
        pass
