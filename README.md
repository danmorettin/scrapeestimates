
## Introduction

This program scrapes analyst estimates from Yahoo Finance and stores them in
a database for each ticker.


## Program Set-Up

This application should be installed using setup.py. From inside the main repo,
run the command in the terminal:
```bash
python setup.py develop
```
Note that the filenames for the logs, tickers, and databases are hard-coded in
so you can call the program from any directory. Update them to your actual
locations.

## Running Program

This application is designed to be run from the command line. After the
project is installed, at the command line type:
```bash
scrapeestimates
```
which will scrape all the tickers in a list, or
```bash
scrapeestimates TSLA
```
if you just want to do one.
If you get warnings from this, you didn't do the program set-up right.

As a backup, the app can be run from inside the main repo as a script:
```bash
python bin/cli.py
```
or
```bash
python bin/cli.py TSLA
```
If you get warnings from this, you didn't do the program set-up right.

The list of tickers to be used is built in *tickers.py*. Edit as desired.

The app will create a sqlite3 database for each ticker, and will add another
row each day you run it.

The app also creates logs that show the success of each ticker. Any failed
tries can be redone using the commands above for single tickers.

## Testing

Test discovery is done from inside the main repo by running the command
```bash
pytest -v
```
