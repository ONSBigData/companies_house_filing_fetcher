# -*- coding: utf-8 -*-
import pandas as pd


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


def companies_to_scrape(basic_info_filepath):

    for df in read_basic_company_data(basic_info_filepath):
        yield from filter_active_and_has_filed(df).to_dict(orient='records')
