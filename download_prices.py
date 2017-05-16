#!/usr/bin/env python3
"""
Download 2 years of historical security data from Yahoo API.
"""
import argparse
import requests
import datetime

from enum import Enum

API_URL = "http://ichart.finance.yahoo.com/table.csv"

class YahooRequestParams:
    SYMBOL = 's'
    INTERVAL = 'g'
    START_MONTH = 'd'
    START_DAY = 'e'
    START_YEAR = 'f'
    END_MONTH = 'a'
    END_DAY = 'b'
    END_YEAR = 'c'


def parse_args():
    def parse_date(s):
        format = "%Y"
        return datetime.datetime.strptime(s, format).date()

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker")
    parser.add_argument("--start_date", "-s", help="Start date (year)", type=parse_date, default=datetime.date.today())
    parser.add_argument("--end_date", "-e", help="End date (year)", type=parse_date, default=datetime.date.today()-datetime.timedelta(days=2 * 7 * 52))
    parser.add_argument("--output", "-o", help="Output file (CSV)", type=argparse.FileType('w'), required=True)

    return parser.parse_args()

def main():
    args = parse_args()
    # http://ichart.finance.yahoo.com/table.csv?s=AAPL&a=1&b=19&c=2010&d=01&e=19&f=2010&g=d&ignore=.csv"
    params = {
        YahooRequestParams.SYMBOL: args.ticker,
        YahooRequestParams.START_MONTH: args.start_date.month,
        YahooRequestParams.START_DAY: args.start_date.day,
        YahooRequestParams.START_YEAR: args.start_date.year,

        YahooRequestParams.END_MONTH: args.end_date.month,
        YahooRequestParams.END_DAY: args.end_date.day,
        YahooRequestParams.END_YEAR: args.end_date.year,
        YahooRequestParams.INTERVAL: 'd', # daily
        'ignore': '.csv'
    }

    answer = requests.get(API_URL, params)
    answer.raise_for_status()
    print(answer.url)
    args.output.write(answer.text)

if __name__ == '__main__':
    main()
