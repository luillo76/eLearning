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

def read_portfolio_values(file_path):
    data = []

    with open(file_path) as file:
        for row in csv.reader(file):
            year, month, day = int(row[0]), int(row[1]), int(row[2])
            dt_op = dt.datetime(year, month, day)
            value = float(row[3])

            data.append((dt_op, value))

    values = np.array(data)

    # Start and End date of the charts
    dt_start = np.min( values[:,0] )
    dt_end = np.max( values[:,0] )

    return values,dt_start,dt_end

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

def get_output(vector):

    # cumulative return
    cum_ret = vector[-1]

    # 
    daily_returns = vector.copy()
    daily_returns[0] = 0

    n_values = len( daily_returns )
    for i in range(1,n_values):
        daily_returns[i] = (vector[i]/vector[i-1]) - 1

    daily_ret = np.mean( daily_returns )
    vol = np.std( daily_returns )
    sharpe = daily_ret/vol * math.sqrt(252)
    
    return sharpe, cum_ret, vol, daily_ret


def print_results(dt_start, dt_end, ls_symbols, na_normalized_price):

    print 'Details of the Performance of the portfolio'

    print 'Data Range : ', dt_start, '  to ', dt_end

    for i in range(0,len(ls_symbols)):
        symbol = ls_symbols[i]
        sharpe, cum_ret, vol, daily_ret = get_output( na_normalized_price[:,i] )

        print ''
        print 'Sharpe Ratio of %s : %s' % (symbol,sharpe)
        print 'Total Return of %s : %s' % (symbol,cum_ret)
        print 'Standard Deviation of %s : %s' % (symbol,vol)
        print 'Average Daily Return of %s : %s' % (symbol,daily_ret)

def plot_results(na_price, outfile_path):

    ldt_timestamps = list(na_price.index)
    na_portfolio = na_price.values
    ls_symbols = list(na_price.columns)

    plt.clf()
    plt.plot(ldt_timestamps, na_portfolio)
    plt.legend('portfolio')
    plt.legend(ls_symbols)
    #plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Fund value')
    plt.savefig(outfile_path, format='pdf')
    #plt.show()

def main(argv):
    values, dt_start, dt_end = read_portfolio_values(argv[0])
    benchmark = argv[1]
    ls_symbols = [benchmark]

    dt_end_read = dt_end + dt.timedelta(days=1)

    d_data = get_symbols_data(ls_symbols, dt_start, dt_end_read)

    # Getting the numpy ndarray of actual close prices
    na_price = d_data['actual_close']

    # insert fund holdings
    na_price.insert(1,'fund',0)
    # factor to scale the benchmark to the initial value of the fund
    scale = values[0,1]/na_price[benchmark].values[0]
    for i in range(0, len(na_price.index)):
        na_price[benchmark].values[i] *= scale
        na_price['fund'].values[i] = values[i,1]

    # Normalizing the prices to start at 1 and see relative returns
    na_normalized_price = na_price.values
    na_normalized_price /= na_normalized_price[0, :]

    ls_symbols = na_price.columns
    print_results(dt_start, dt_end, ls_symbols, na_normalized_price)

    outfile_path = argv[0]+".pdf"
    
    plot_results(na_price, outfile_path)

if __name__ == "__main__":
    main(sys.argv[1:])
