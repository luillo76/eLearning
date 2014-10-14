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

    orders = np.array(data)

    ls_symbols = list(set( orders[:,1] ))

    # Start and End date of the charts
    dt_start = np.min( orders[:,0] )
    dt_end = np.max( orders[:,0] )

    return orders,ls_symbols,dt_start,dt_end

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

def print_results(dt_start, dt_end):
    print 'The final value of the portfolio using the sample file is -- 2011,12,20,1133860'
    print 'Data Range :  ', dt_start,'  to ', dt_end

def main(argv):
    initial_cash = float(argv[0])
    orders, ls_symbols, dt_start, dt_end = read_orders(argv[1])
    fname = argv[2]

    dt_end_read = dt_end + dt.timedelta(days=1)

    d_data = get_symbols_data(ls_symbols, dt_start, dt_end_read)

    # Getting the numpy ndarray of actual close prices
    na_price = d_data['actual_close']

    na_portfolio = get_portfolio_value(initial_cash, orders, na_price)

    write_portfolio(fname, na_portfolio)
    print_results(dt_start, dt_end_read)

if __name__ == "__main__":
    main(sys.argv[1:])
