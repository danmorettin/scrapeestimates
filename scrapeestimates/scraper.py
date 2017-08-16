
"""This module scrapes the analyst estimates from Yahoo Finance and the number
of shares outstanding from Reuters."""

import requests
from lxml import html

from scrapeestimates.regex import parse_number, parse_percent


class Scraper():
    """Scrapes the analyst estimates and shares outstanding.

    Attributes:
        ticker: A string with the ticker.
        scraped_data: A dictionary with the scraped data. Available after
                      calling scrape.
    """

    def __init__(self, ticker):
        """Inits Scraper with the ticker of interest."""
        self.ticker = ticker
        self.parser_estimates = None
        self.parser_shares = None
        self.shares = None
        self.data = None
        self.scraped_data = None

    def scrape(self):
        """Calls each of the private functions in the required order. Then
        stores the data in a dict."""
        self._download_estimates()
        self._download_shares()
        self._parse_shares()
        self._parse_estimates()

        scraped_data = self.data
        scraped_data['shares'] = self.shares
        self.scraped_data = scraped_data

    def _download_estimates(self):
        url = ('https://finance.yahoo.com/quote/{}/' +
               'analysts?p={}').format(self.ticker, self.ticker)
        response = requests.get(url)
        # print(response.text)
        self.parser_estimates = html.fromstring(response.text)

    def _download_shares(self):
        url = ('http://www.reuters.com/finance/stocks/overview?symbol=' +
               '{}').format(self.ticker.replace('-', ''))
        response = requests.get(url)
        # print(response.text)
        self.parser_shares = html.fromstring(response.text)

    def _parse_shares(self):
        shares = self.parser_shares.xpath(
            '//div[@id="overallRatios"]//tr[3]//td[2]/node()/text()')[0]
        self.shares = float(shares.replace(',', '')) * 1000000

    def _parse_estimates(self):
        last_year_eps = self.parser_estimates.xpath(
            '//span[@data-reactid="85"]/text()')[0]
        current_year_eps = self.parser_estimates.xpath(
            '//span[@data-reactid="52"]/text()')[0]
        next_year_eps = self.parser_estimates.xpath(
            '//span[@data-reactid="54"]/text()')[0]

        last_year_rev = self.parser_estimates.xpath(
            '//span[@data-reactid="166"]/text()')[0]
        current_year_rev = self.parser_estimates.xpath(
            '//span[@data-reactid="133"]/text()')[0]
        next_year_rev = self.parser_estimates.xpath(
            '//span[@data-reactid="135"]/text()')[0]

        EPS_GROWTH_INDEX = 16
        eps_growth = self.parser_estimates.xpath(
            '//td[@class="Ta(end) Py(10px)"]/text()')[EPS_GROWTH_INDEX]

        data = {}
        data['last_year_rev'] = last_year_rev
        data['current_year_rev'] = current_year_rev
        data['next_year_rev'] = next_year_rev
        data['last_year_eps'] = last_year_eps
        data['current_year_eps'] = current_year_eps
        data['next_year_eps'] = next_year_eps
        data['eps_growth'] = eps_growth

        # print(data)
        self.data = self._parse_data(data)

    def _parse_data(self, data):
        try:
            lyeps = float(data['last_year_eps'])
        except:
            lyeps = 0
        data['last_year_eps'] = lyeps
        data['current_year_eps'] = float(data['current_year_eps'])
        data['next_year_eps'] = float(data['next_year_eps'])

        try:
            lyrev = parse_number(data['last_year_rev'])
        except:
            lyrev = 0
        data['last_year_rev'] = lyrev
        data['current_year_rev'] = parse_number(data['current_year_rev'])
        data['next_year_rev'] = parse_number(data['next_year_rev'])

        try:
            lyepsg = parse_percent(data['eps_growth'])
        except:
            lyepsg = 0
        data['eps_growth'] = lyepsg
        return data


def _test():
    ticker = 'AAPL'       # 'MRK', 'BAM-A.TO', 'TRI.TO'
    print('Downloading data for {}'.format(ticker))
    test_data = Scraper(ticker)
    test_data.scrape()
    print(test_data.scraped_data)


if __name__ == "__main__":
    _test()
