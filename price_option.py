#!/usr/bin/env python3
"""
Price an option using half of the historical data, then compute to see how much
we would have earned.
"""

import argparse
import csv
import statistics
import datetime
from math import *
import matplotlib.pyplot as plt

DATE_FMT = '%Y-%m-%d'

def N(x):
    """
    Cumulative distribution function for the standard normal distribution
    """
    return (1.0 + erf(x / sqrt(2.0))) / 2.0


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_file", type=argparse.FileType(), help="Data file (CSV)")
    # TODO maybe this should be 1.03
    parser.add_argument("-r", type=float, help="Risk free return (default 0.03)", default=0.03)
    parser.add_argument("--strike", "-k", type=float, help="Strike price (default = price at emission time)")
    parser.add_argument("--plot", "-p", help="Plot to file instead of showing the plot.")

    return parser.parse_args()


def date(row):
    """
    Returns the date for the given data row
    """
    return datetime.datetime.strptime(row['Date'], '%Y-%m-%d').date()


def price_call_option(historical_data, K, r, T):
    """
    Returns the call option price calculated using historical data.
    The option is set to expire in T years, have a strike price of K. The risk
    free rate is r.
    """
    # Use last open as spot price
    S = float(historical_data[-1]['Open'])
    volatility = statistics.stdev(float(d['Open']) for d in historical_data)

    d1 = log(S / K) + 0.5 * volatility ** 2 * (T) / (volatility * sqrt(T))
    d2 = d1 - volatility * sqrt(T)

    # Price for a call option
    C = S * N(d1) - K * exp(-r * T) * N(d2)

    return C

def separate_historical_and_testing(data):
    """
    Cut the given data in half the first half for estimation and the second for
    testing.
    """
    start_date = date(data[0])
    stop_date = date(data[-1])

    write_time = start_date + (stop_date - start_date) / 2

    estimation_data = [d for d in data if date(d) < write_time]
    future_data = [d for d in data if date(d) >= write_time]

    return estimation_data, future_data

def main():
    args = parse_args()

    data = list(csv.DictReader(args.data_file))

    # Make sure data are sorted in ascending order
    data.sort(key=lambda s: s['Date'])

    # Extracts data used for volatility estimation
    estimation_data, future_data = separate_historical_and_testing(data)

    # Compute black schole pricing
    # TODO Is open the good estimator ?
    volatility = statistics.stdev(float(d['Open']) for d in estimation_data)

    r = args.r

    if args.strike:
        K = args.strike
    else:
        K = S

    # Compute the time interval in years (T - t in the book)
    write_time = date(estimation_data[-1])
    stop_date = date(future_data[-1])

    # Compute exercise time in year
    T = (stop_date - write_time).days / 365

    C = price_call_option(estimation_data, K, r, T)

    print("Computing option price on {} for an exercise in {:.1f} years".format(write_time, T))
    print("Volatility σ = {:.2f}".format(volatility))
    print("Strike price K = {:.1f}".format(K))
    print("Call price = {:.1f}".format(C))
    print("Risk free rate: {:.2f}".format(r))

    # Plot a few things
    x  = [date(d) for d in data]
    y  = [float(d['Open']) for d in data]
    plt.plot(x, y)

    # Draw a line at write time time
    plt.axvline(x=write_time, color='r', linestyle='dotted')

    # Draw a line at the strike price
    plt.axhline(y=K, color='b', linestyle='dotted')

    plt.xlabel('Date')
    plt.ylabel('Price [$]')
    plt.title('Call price: {:.1f} $'.format(C))
    plt.legend(['Underlying', 'Option writing', 'Strike'])


    if args.plot:
        plt.savefig(args.plot)
    else:
        plt.show()

if __name__ == '__main__':
    main()
