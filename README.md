
## Introduction

This program scrapes analyst estimates from Yahoo Finance and stores them in
a database for each ticker.


## Program Set-Up

This application should be installed using setup.py. From inside the main repo,
run the command in the terminal:
```bash
python setup.py develop
```


## Running Program

This application is designed to be run from the command line. After the
project is installed, at the command line type:
```bash
scrapeestimates
```
if you want to scrape all the items in a list, or
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

Test discovery is done from inside the main repo by running the command
```bash
py.test
```
