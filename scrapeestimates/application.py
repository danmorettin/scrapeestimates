
"""application.py

This module does two things: 1) abstracts the application into a class, and
2) provides the main entry point for the application.

A flowchart of the high level execution steps is included in the flowchart
directory.

Note that the filenames for the logs, tickers, and databases are hard-coded
so that you can start the program from any directory. Update them before use.
"""

import logging
from datetime import date
from random import random
from sys import argv
from time import sleep

from scrapeestimates.database import DatabaseManager
from scrapeestimates.scraper import Scraper
from scrapeestimates.tickers import Tickers


def main():
    """Main entry point for console_scripts."""
    app = Application(argv)
    app.run()


class Application():
    """Abstracts the application into a class."""
    def __init__(self, argv):
        """Inits with the ticker of interest (if desired), otherwise the
        application will compile a list of tickers from csv files"""
        try:
            self.ticker = str(argv[1])
        except:
            pass

    def run(self):
        """Compliles the list of tickers (if applicable), then for each ticker,
        a database is created (or connected to), then the estimates are
        scraped, then the data is added to a new row in the database. Key steps
        are logged and written to file.
        """
        today = date.today()
        filename = ('/Users/Dan/Coding/Finance/projects/scrapeestimates/' +
                    'data/logs/{}').format(today)
        SCRAPE_DELAY = 2 + 2 * random()

        logging.basicConfig(filename=filename,
                            level=logging.INFO,
                            format='%(asctime)s : %(levelname)s : %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.getLogger('requests').setLevel(logging.CRITICAL)

        logging.info('Program started.')

        try:
            tickers = [self.ticker]
        except:
            symbols = Tickers()
            symbols.get_ticker_list()
            tickers = symbols.ticker_list
        tickers = ['MRK']   # do a test ticker to make sure working
        # print(tickers)

        error_list = []
        count = 0
        for ticker in tickers:
            count += 1
            print('{} of {}'.format(count, len(tickers)))
            logging.info('{} of {}'.format(count, len(tickers)))

            try:
                filename = ('/Users/Dan/Coding/Finance/projects/' +
                            'scrapeestimates/data/databases/{}.db').format(
                            ticker)
                db = DatabaseManager(ticker, filename)
                logging.info(('Successfully instantiated database manager ' +
                             'for {}.').format(ticker))
            except Exception as e:
                logging.error(('Error instantiating database manager ' +
                              'for {}.').format(ticker))
                logging.error(e)
            else:
                try:
                    estimate_scraper = Scraper(ticker)
                    estimate_scraper.scrape()
                    data = estimate_scraper.scraped_data
                    data['date'] = date.today()
                    logging.info(('Successfully scraped and parsed data ' +
                                 'for {}.').format(ticker))
                except Exception as e:
                    error_list.append(ticker)
                    logging.error(('Error scraping and parsing data ' +
                                  'for {}.').format(ticker))
                    logging.error(e)
                else:
                    try:
                        db.add_row(data)
                        logging.info(('Successfully added {} data to ' +
                                     'database.').format(ticker))
                    except Exception as e:
                        logging.error(('Error adding {} data to ' +
                                      'database.').format(ticker))
                        logging.error(e)
            db.close()
            sleep(SCRAPE_DELAY)
        print('Stocks not added to database include: ', error_list)
