# -*- coding: utf-8 -*-
"""
@author: Philip Lee
"""
import os
import filing_fetcher.companies

POSSIBLE_PATHS = ["tests/resources", "resources", ""]

def fetch_resource(filename):
    """Searches through possible locations for test resources.
    Not ideal, relative location of test resources depends on how pytest is run.
    """

    for path in POSSIBLE_PATHS:

        filepath = os.path.join(path, filename)

        if os.path.isfile(filepath):
            return filepath

    return None


def test_companies_to_scrape():

    filepath = fetch_resource('BasicCompanyDataAsOneFileTest.csv')
    companies_to_scrape = filing_fetcher.companies.companies_to_scrape(filepath)

    result = list(map(lambda x: x['CompanyNumber'], companies_to_scrape))

    expected = [
        'TESTA001',
        'TESTB002',
        'TESTC003',
        'TESTD004',
        'TESTE005',
    ]

    assert result == expected
