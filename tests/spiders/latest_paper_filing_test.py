# -*- coding: utf-8 -*-
"""
@author: Philip Lee
"""
import filing_fetcher.spiders.latest_paper_filing
from tests.http_response_from_file import dummy_http_response


def test_simple_filing_history():

    meta = {'CompanyNumber': 'somenumber'}

    spider = filing_fetcher.spiders.latest_paper_filing.LatestPaperFilingSpider()

    response = dummy_http_response('simple_filing_history.json', meta)

    item_generator = spider.parse_filing_history(response)

    expected = ['2018-03-15']
    result = [item['made_up_date'] for item in item_generator]

    assert result == expected
