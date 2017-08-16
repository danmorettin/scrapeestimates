
"""database.py

This module contains a database manager that acts as an ORM.
"""

import pandas
import sqlite3


class DatabaseManager():
    """Abstracts away the SQL statements.

    Attributes:
        conn: The connection to the database. conn is closed by __del__ if
              close() is forgotten.
        cur: The cursor for the database.
    """
    def __init__(self, ticker, filename):
        """Inits with the ticker of interest."""
        self.conn = sqlite3.connect(filename,
                                    detect_types=sqlite3.PARSE_DECLTYPES |
                                    sqlite3.PARSE_COLNAMES)
        self.cur = self.conn.cursor()

    def __del__(self):
        if self.conn:
            self.conn.close()

    def create_table(self):
        """Creates the table if it does not exist. Does nothing if it already
        exists."""
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Estimates (
                        'date' DATE PRIMARY KEY,
                        'last_year_rev' REAL,
                        'current_year_rev' REAL,
                        'next_year_rev' REAL,
                        'last_year_eps' REAL,
                        'current_year_eps' REAL,
                        'next_year_eps' REAL,
                        'eps_growth' REAL,
                        'shares' REAL
                        )""")
        self.conn.commit()

    def add_row(self, data):
        """Adds a row into the database with the scraped data."""
        self.create_table()
        try:
            self.cur.execute("""INSERT INTO Estimates VALUES (
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?
                            )""", (data['date'],
                                   data['last_year_rev'],
                                   data['current_year_rev'],
                                   data['next_year_rev'],
                                   data['last_year_eps'],
                                   data['current_year_eps'],
                                   data['next_year_eps'],
                                   data['eps_growth'],
                                   data['shares']))
            self.conn.commit()
        except Exception as e:
            print('That date already exists in the database.')
            raise RuntimeError('That date already exists in the database.')

    def get_data(self):
        """Retrieves the all the estimates stored an returns them as a single
        pandas dataframe."""
        self.df = pandas.read_sql_query("SELECT * FROM Estimates", self.conn)

    def close(self):
        """Closes the conn"""
        if self.conn:
            self.conn.close()


def _test():
    from datetime import date
    from datetime import timedelta
    ticker = 'TEST'
    filename = ('/Users/Dan/Coding/Finance/projects/' +
                'scrapeestimates/data/test_data/{}.db').format(
                ticker)
    today = date.today()
    db = DatabaseManager(ticker, filename)
    db.create_table()

    diction = {'date': today,
               'last_year_rev': 149.23,
               'current_year_rev': 226.65,
               'next_year_rev': 253.74,
               'last_year_eps': 8.31,
               'current_year_eps': 8.94,
               'next_year_eps': 10.57,
               'eps_growth': 11.07,
               'shares': 100}
    db.add_row(diction)

    diction = {'date': today - timedelta(days=1),
               'last_year_rev': 149.23,
               'current_year_rev': 226.65,
               'next_year_rev': 253.74,
               'last_year_eps': 8.31,
               'current_year_eps': 8.94,
               'next_year_eps': 10.57,
               'eps_growth': 11.07,
               'shares': 100}
    db.add_row(diction)
    db.get_data()
    print(db.df)
    print(db.df.at[0, 'current_year_rev'])
    db.close()


if __name__ == "__main__":
    _test()
