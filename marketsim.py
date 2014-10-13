import sys
import csv
import random
import math

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def read_orders(file_path):
    data = []

    with open(file_path) as file:
        for row in csv.reader(file):
            year, month, day = int(row[0]), int(row[1]), int(row[2])
            dt_op = dt.datetime(year, month, day)
            buy = 1
            if( row[4]=="SELL"): buy = -1
            value = float(row[5])
            
            data.append((dt_op, row[3], value*buy))

    array = np.array(data)
    return array

def get_symbols_data(ls_symbols, dt_start, dt_end):

    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)

    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # Filling the data for NAN
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    return d_data


def get_portfolio_value(initial_cash, orders, na_price):

    na_portfolio = na_price.copy()
    na_portfolio.values.fill(0)
    na_portfolio.insert(0,'cash', initial_cash)

    for order_day, sym, nshares in orders:
        prize = -999

        for i in range(0,len(na_portfolio.index)):
            day = na_portfolio.index[i]
            if( (day-order_day).days >= 0):
                na_portfolio[sym].values[i] += nshares
                if(prize < 0):
                    prize = na_price[sym].values[i]
                na_portfolio['cash'].values[i] += (-nshares*prize)


    for sym in na_price.columns:
        na_portfolio[sym] *= na_price[sym]

    na_portfolio.insert(0,'total', na_portfolio['cash'])
    for sym in na_price.columns:
        na_portfolio['total'] += na_portfolio[sym]

    return na_portfolio

def write_portfolio(file_path, na_portfolio):

    with open(file_path, mode='w') as file:
        csv_writer = csv.writer(file)

        for i in range(0,len(na_portfolio.index)):
            date = na_portfolio.index[i]
            year = date.year
            month = date.month
            day = date.day
            value = na_portfolio['total'].values[i]
            
            row_to_enter = [year,month,day, value]
            csv_writer.writerow(row_to_enter)

    return

def run_simulation(data):
    success = 0

    for params in data:
        if random.gauss(params[0], params[1]) > 0:
            success += 1

    return success


def print_results(results):
    print
    print '           Minimum: %s' % (np.amin(results))
    print '   25th Percentile: %s' % (np.percentile(results, 25))
    print '            Median: %s' % (np.median(results))
    print '   75th Percentile: %s' % (np.percentile(results, 75))
    print '           Maximum: %s' % (np.amax(results))
    print
    print '              Mean: %s' % (np.mean(results))
    print 'Standard Deviation: %s' % (np.std(results))
    print '          Variance: %s' % (np.var(results))
    print
    print '           Victory: %s' % (float(sum(i > 20 for i in results)) / len(results))
    print


def plot_results(results):
    plt.hist(results, bins = (np.amax(results) - np.amin(results)), normed = True)
    plt.title('Election Results')
    plt.xlabel('Margin')
    plt.ylabel('Probability')
    plt.show()


def main(argv):
    initial_cash = float(argv[0])
    orders = read_orders(argv[1])
    fname = argv[2]

    ls_symbols = orders[:,1]
    #TODO: should remove replicas
    ls_symbols = ['AAPL', 'IBM']

    # Start and End date of the charts
    dt_start = dt.datetime(2008, 12, 1)
    dt_end = dt.datetime(2008, 12, 10)

    d_data = get_symbols_data(ls_symbols, dt_start, dt_end)

    # Getting the numpy ndarray of actual close prices
    na_price = d_data['actual_close']

    na_portfolio = get_portfolio_value(initial_cash, orders, na_price)

    write_portfolio(fname, na_portfolio)

    results   = []
#    for _ in xrange(int(argv[1])):
#        results.append(run_simulation(data))
#
#    print_results(results)
#    plot_results(results)


if __name__ == "__main__":
    main(sys.argv[1:])
