
"""This module compiles a list of stock tickers from csv files."""

import pandas
from os import path, getcwd


class Tickers():
    """Compiles a list of tickers.

    Attributes:
        ticker_list: A list with tickers as strings.
    """

    def __init__(self):
        """Inits Tickers with an empty list."""
        self.ticker_list = []

    def get_ticker_list(self):
        """Runs through a list of csv files to put the tickers in a list. Then
        removes duplicates."""
        filenames = [
            ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
             'data/tickers/canada.csv'),
            ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
             'data/tickers/aerospace.csv'),
            ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
             'data/tickers/consumer_discretionary.csv'),
            ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
             'data/tickers/consumer_staples.csv'),
            ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
             'data/tickers/energy.csv'),
            ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
             'data/tickers/financial.csv'),
            ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
             'data/tickers/healthcare.csv'),
            ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
             'data/tickers/industrial.csv'),
            ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
             'data/tickers/materials.csv'),
            ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
             'data/tickers/mining.csv'),
            ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
             'data/tickers/real_estate.csv'),
            ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
             'data/tickers/retail.csv'),
            ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
             'data/tickers/technology.csv'),
            ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
             'data/tickers/telecom.csv'),
            ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
             'data/tickers/transports.csv'),
            ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
             'data/tickers/utilities.csv')
        ]

        for filename in filenames:
            tickers = self._get_batch_of_tickers(filename)
            self.ticker_list = self.ticker_list + tickers

        # Remove duplicates
        self.ticker_list = list(set(self.ticker_list))

    def _get_batch_of_tickers(self, filename):
        filepath = path.abspath(path.join(
            getcwd(), filename))
        df = pandas.read_csv(filepath)
        tickers = []
        for index, row in df.iterrows():
            tickers.append(row['Ticker'])
        return tickers


def _test():
    symbols = Tickers()
    symbols.get_ticker_list()
    print(symbols.ticker_list)


if __name__ == "__main__":
    _test()
