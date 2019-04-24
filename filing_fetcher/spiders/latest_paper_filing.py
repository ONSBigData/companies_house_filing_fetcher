# -*- coding: utf-8 -*-
import configparser
import json
import logging
import os

import scrapy

import filing_fetcher.items
import filing_fetcher.companies
import filing_fetcher.configuration


def fetch_auth():
    auth_config_path = os.path.join(os.path.expanduser('~'), 'config', 'ch_api_key.ini')

    config = configparser.ConfigParser()
    config.read(auth_config_path)

    return config['companies_house']['key']


CH_AUTH = fetch_auth()

logger = logging.getLogger(__name__)

config = filing_fetcher.configuration.get_config()

FILING_HISTORY_URL = 'https://api.companieshouse.gov.uk/company/{}/filing-history?category=accounts'


class LatestPaperFilingSpider(scrapy.spiders.CrawlSpider):
    name = 'latest_paper_filing'
    allowed_domains = ['api.companieshouse.gov.uk']

    http_user = CH_AUTH
    http_pass = ''

    def start_requests(self):
        """Generates crawler request for given base URL and parse results."""
        logger.info(f"Reading basic company info from: {config.BASIC_COMPANY_INFO_FILEPATH}")

        companies_to_scrape = filing_fetcher.companies.companies_to_scrape(config.BASIC_COMPANY_INFO_FILEPATH)

        for i, company_info in enumerate(companies_to_scrape):
            logger.debug(f"Request {i} - {company_info}")
            company_number = company_info["CompanyNumber"]

            yield scrapy.Request(
                url=FILING_HISTORY_URL.format(company_number),
                meta=company_info,
                callback=self.parse_filing_history
            )

    def parse_filing_history(self, response):

        def set_if_present(item, name, data, path):
            try:
                item[name] = data[path]
            except KeyError:
                logger.warning(f"{path} not found in {data}")

        filing_item = filing_fetcher.items.FilingItem()

        set_if_present(filing_item, 'company_number', response.meta, 'CompanyNumber')
        set_if_present(filing_item, 'company_status', response.meta, 'CompanyStatus')
        set_if_present(filing_item, 'incorporation_date', response.meta, 'IncorporationDate')
        set_if_present(filing_item, 'accounts_next_due_date', response.meta, 'Accounts.NextDueDate')
        set_if_present(filing_item, 'accounts_last_made_up_date', response.meta, 'Accounts.LastMadeUpDate')
        set_if_present(filing_item, 'accounts_account_category', response.meta, 'Accounts.AccountCategory')

        json_response = json.loads(response.body_as_unicode())

        set_if_present(filing_item, 'filing_history_status', json_response, 'filing_history_status')

        if 'items' in json_response:

            relevant_items = [item for item in json_response['items'] if item['type'] in ['AA', 'AAMD', 'BS']]

            sorted_items = list(reversed(sorted(relevant_items, key=lambda x: x['date'])))

            if len(sorted_items) > 0:
                most_recent_filing = sorted_items[0]

                set_if_present(filing_item, 'pages', most_recent_filing, 'pages')
                set_if_present(filing_item, 'date', most_recent_filing, 'date')
                set_if_present(filing_item, 'type', most_recent_filing, 'type')
                set_if_present(filing_item, 'barcode', most_recent_filing, 'barcode')

                try:
                    filing_item["made_up_date"] = most_recent_filing["description_values"]["made_up_date"]
                except KeyError:
                    pass

                if 'paper_filed' in most_recent_filing and most_recent_filing['paper_filed']:

                    filing_item['file_urls'] = [most_recent_filing['links']['document_metadata'] + '/content']

        yield filing_item
