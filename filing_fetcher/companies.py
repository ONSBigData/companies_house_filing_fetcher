# -*- coding: utf-8 -*-
"""
@author: Philip Lee
"""
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

    df = pd.read_csv(filepath, usecols=relevant_columns, dtype={' CompanyNumber': str})

    df = df.rename(columns={' CompanyNumber': 'CompanyNumber'})

    return df


def companies_to_scrape(basic_info_filepath):

    df = read_basic_company_data(basic_info_filepath)

    return df.sample(n=1000).iloc[:1000].to_dict(orient='records')
