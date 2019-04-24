# -*- coding: utf-8 -*-
import os

import pandas as pd

import filing_fetcher.configuration

config = filing_fetcher.configuration.get_config()

_digital_reporters = None


def digital_reporters():
    global _digital_reporters

    if _digital_reporters is None:
        df = pd.read_csv(config.DIGITAL_REPORTERS_FILEPATH, dtype={"crn": str})
        _digital_reporters = set(df.crn)

    return _digital_reporters


_already_seen = None


def already_seen():
    global _already_seen

    if _already_seen is None:
        if os.path.isfile(config.LATEST_FILING_FEED_FILE):
            df = pd.read_json(config.LATEST_FILING_FEED_FILE, orient='records', lines=True)

            if len(df) > 0:
                _already_seen = set(df.company_number)
            else:
                _already_seen = set()
        else:
            _already_seen = set()

    return _already_seen


def read_basic_company_data(filepath):

    relevant_columns = [
        ' CompanyNumber',
        'CompanyStatus',
        'IncorporationDate',
        'Accounts.NextDueDate',
        'Accounts.LastMadeUpDate',
        'Accounts.AccountCategory'
    ]

    dfs = pd.read_csv(filepath, usecols=relevant_columns, dtype={' CompanyNumber': str}, chunksize=100000)

    for df in dfs:
        df = df.rename(columns={' CompanyNumber': 'CompanyNumber'})

        yield df


def filter_active_and_has_filed(df):
    return df[df.CompanyStatus.str.startswith('Active') & df['Accounts.LastMadeUpDate'].notnull()]


def remove_digital_reporters(df):
    return df[~df.CompanyNumber.isin(digital_reporters())]


def remove_already_seen(df):
    return df[~df.CompanyNumber.isin(already_seen())]


def companies_to_scrape(filepath):

    for df in read_basic_company_data(filepath):

        df = filter_active_and_has_filed(df)
        df = remove_digital_reporters(df)
        df = remove_already_seen(df)

        yield from df.to_dict(orient='records')


if __name__ == '__main__':

    print(len(list(companies_to_scrape())))