#!/usr/bin/env python3
"""
Implement a simple backtesting over several actions to see if the option
pricing is really fair (i.e. both side of the deal share the risk).
"""

import argparse
import price_option
import csv
import statistics


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('data_file', nargs='+', type=argparse.FileType())
    parser.add_argument(
        "-r", type=float, help="Risk free return (default 1.03)", default=1.03)
    parser.add_argument(
        "--strike",
        "-k",
        type=float,
        help="Strike price (default = price at emission time)")

    return parser.parse_args()


def main():
    args = parse_args()

    payoffs = []

    for data_file in args.data_file:
        data = list(csv.DictReader(data_file))

        # Make sure data are sorted in ascending order
        data.sort(key=lambda s: s['Date'])

        estimation_data, testing_data = price_option.separate_historical_and_testing(
            data)

        S = float(estimation_data[-1]['Open'])

        if args.strike:
            K = args.strike
        else:
            K = S

        write_time = price_option.date(estimation_data[-1])
        stop_date = price_option.date(testing_data[-1])

        # Compute exercise time in year
        T = (stop_date - write_time).days / 365

        # Compute option price
        C = price_option.price_call_option(estimation_data, K, args.r, T)

        # Compute buyer payoff
        Sf = float(testing_data[-1]['Open'])  # final price

        # TODO: Is the payoff formula correct
        buyer_payoff = max(0, Sf - K) - C

        payoffs.append((K, C, buyer_payoff))

        print("{}: buyer_payoff = {:.2f}".format(data_file.name, buyer_payoff))

    mean = statistics.mean(1 + (p / (C + K)) for (K, C, p) in payoffs)
    print("Mean relative return: {}".format(mean))


if __name__ == '__main__':
    main()
