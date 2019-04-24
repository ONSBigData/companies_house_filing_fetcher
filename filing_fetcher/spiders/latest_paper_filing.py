# -*- coding: utf-8 -*-
import configparser
import json
import logging
import os

import scrapy

import filing_fetcher.items

CONFIG_PATH = os.path.join(os.path.expanduser('~'), 'config', 'ch_api_key.ini')
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

CH_AUTH = config['companies_house']['key']

logger = logging.getLogger(__name__)


class LatestPaperFilingSpider(scrapy.spiders.CrawlSpider):
    name = 'latest_paper_filing'
    allowed_domains = ['api.companieshouse.gov.uk']

    http_user = CH_AUTH
    http_pass = ''

    def parse_filing_history(self, response):
        json_response = json.loads(response.body_as_unicode())

        if 'items' in json_response:

            relevant_items = [item for item in json_response['items'] if item['type'] in ['AA', 'AAMD', 'BS']]

            sorted_items = list(reversed(sorted(relevant_items, key=lambda x: x['date'])))

            if len(sorted_items) > 0:
                most_recent_filing = sorted_items[0]

                if 'paper_filed' in most_recent_filing and most_recent_filing['paper_filed']:
                    paper_filing_item = filing_fetcher.items.FilingItem()

                    paper_filing_item['company_number'] = response.meta['CompanyNumber']
                    paper_filing_item['file_urls'] = [most_recent_filing['links']['document_metadata'] + '/content']

                    paper_filing_item['pages'] = most_recent_filing['pages']
                    paper_filing_item['date'] = most_recent_filing['date']
                    paper_filing_item['type'] = most_recent_filing['type']
                    paper_filing_item['barcode'] = most_recent_filing['barcode']

                    try:
                        paper_filing_item["made_up_date"] = most_recent_filing["description_values"]["made_up_date"]
                    except KeyError:
                        pass

                    yield paper_filing_item
                else:

                    made_up_date = most_recent_filing["description_values"]["made_up_date"]
                    logger.debug(f'No paper filing for {response.meta["CompanyNumber"]},'
                                 f' date: {most_recent_filing["date"]}, made_up_date: {made_up_date}')

        else:
            try:
                print(json_response['filing_history_status'])
            except KeyError:
                pass
