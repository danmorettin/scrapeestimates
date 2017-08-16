
""" run 'pytest -v' at the command line in the main directory """

import os
from datetime import date
from datetime import timedelta

from scrapeestimates.regex import parse_number, parse_percent
from scrapeestimates.tickers import Tickers
from scrapeestimates.database import DatabaseManager
from scrapeestimates.scraper import Scraper


class TestTickersModule():

    def test_parse_number(self):
        tickers = Tickers()
        tickers.get_ticker_list()
        assert 'TSLA' in tickers.ticker_list
        assert 'GE' in tickers.ticker_list
        assert 'TD.TO' in tickers.ticker_list


class TestRegexModule():

    def test_parse_number(self):
        assert parse_number('123.45B') == float(123450000000)
        assert parse_number('123.45M') == float(123450000)
        assert parse_number('123B') == float(123000000000)
        assert parse_number('123M') == float(123000000)
        assert parse_number('1B') == float(1000000000)
        assert parse_number('1M') == float(1000000)

    def test_parse_percent(self):
        assert parse_percent('11.07%') == float(11.07)
        assert parse_percent('11%') == float(11)


class TestScraperModule():

    def test_scrape_US_ticker(self):
        ticker = 'AAPL'
        test_data = Scraper(ticker)
        test_data.scrape()
        values_in_dict = test_data.scraped_data
        assert values_in_dict.get('next_year_rev')

    def test_scrape_CAN_ticker(self):
        ticker = 'TD.TO'
        test_data = Scraper(ticker)
        test_data.scrape()
        values_in_dict = test_data.scraped_data
        assert values_in_dict.get('next_year_rev')

    def test_scrape_CAN_dash_ticker(self):
        ticker = 'BAM-A.TO'
        test_data = Scraper(ticker)
        test_data.scrape()
        values_in_dict = test_data.scraped_data
        assert values_in_dict.get('next_year_rev')


class TestDatabaseModule():

    def setup(self):
        self.ticker = 'TEST'
        try:
            name = ('/Users/Dan/Coding/Finance/projects/' +
                    'scrapeestimates/data/test_data/{}.db'.format(
                     self.ticker))
            os.remove(name)
        except:
            pass

    def teardown(self):
        try:
            name = ('/Users/Dan/Coding/Finance/projects/' +
                    'scrapeestimates/data/test_data/{}.db'.format(
                     self.ticker))
            os.remove(name)
        except:
            pass

    def test_database_manager_with_new_database(self):
        filename = ('/Users/Dan/Coding/Finance/projects/' +
                    'scrapeestimates/data/test_data/{}.db').format(
                    self.ticker)
        today = date.today()
        db = DatabaseManager(self.ticker, filename)
        db.create_table()
        test_dict_1 = {'date': today,
                       'last_year_rev': 149.23,
                       'current_year_rev': 226.65,
                       'next_year_rev': 253.74,
                       'last_year_eps': 8.31,
                       'current_year_eps': 8.94,
                       'next_year_eps': 10.57,
                       'eps_growth': 11.07,
                       'shares': 100}
        db.add_row(test_dict_1)
        test_dict_2 = {'date': today - timedelta(days=1),
                       'last_year_rev': 149.23,
                       'current_year_rev': 226.65,
                       'next_year_rev': 253.74,
                       'last_year_eps': 8.31,
                       'current_year_eps': 8.94,
                       'next_year_eps': 10.57,
                       'eps_growth': 11.07,
                       'shares': 100}
        db.add_row(test_dict_2)
        db.get_data()
        assert db.df.at[0, 'current_year_rev'] == 226.65
        db.close()

    def test_database_manager_with_existing_database(self):
        filename = ('/Users/Dan/Coding/Finance/projects/' +
                    'scrapeestimates/data/test_data/ADBE.db')
        db = DatabaseManager('ADBE', filename)
        db.create_table()
        db.get_data()
        assert db.df.at[0, 'current_year_rev'] == 7210000000.0
        db.close()
