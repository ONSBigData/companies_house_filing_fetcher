# Companies House filings fetcher

Downloads paper filings from the Companies House API

## Usage

    scrapy crawl latest_paper_filing
    
## Set up

**Assumptions**:

* Conda package manager installed

**Steps**:

Clone the project:

```shell
    clone git@github.com:ONSBigData/companies_house_filing_fetcher.git
```

Set up the Python environment:

```shell
    cd companies_house_filing_fetcher
    conda env create -f environment.yml
    conda activate pdf_downloader
```

Copy the config files to `~/config` and edit their contents:

```shell
    mkdir ~/config
    cp ch_api_key.example.ini ~/config/ch_api_key_example.ini
    cp filing_fetcher_config.example.yml ~/config/filing_fetcher_config.yml
```

Review config values in `spiders/settings.py`.
    
Run the downloader:

```shell
    scrapy crawl latest_paper_filing
```
