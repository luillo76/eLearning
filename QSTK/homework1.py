'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on January, 24, 2013

@author: Sourabh Bajaj
@contact: sourabhbajaj@gatech.edu
@summary: Example tutorial code.
'''

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

import numpy as np 
import math

print "Pandas Version", pd.__version__

def simulate(dt_start, dt_end, ls_symbols, weights, _print_):

    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    # Creating an object of the dataaccess class with Yahoo as the source.
    #c_dataobj = da.DataAccess('Yahoo')
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

    # Getting the numpy ndarray of close prices.
    na_price = d_data['close'].values

    # Normalizing the prices to start at 1 and see relative returns
    na_normalized_price = na_price / na_price[0, :]

    n_symbols = len(ls_symbols)
    for i in range(0,n_symbols):
        symbol = ls_symbols[ i ]
        weight = weights [ i ]
        na_normalized_price[:, i] = na_normalized_price[:, i] * weight

    na_portfolio = na_normalized_price[:, 0]
    for i in range(1,n_symbols):
        na_portfolio += na_normalized_price[:, i]

    # cumulative return
    cum_ret = na_portfolio[-1]

    # 
    daily_returns = na_portfolio.copy()
    daily_returns[0] = 0

    n_values = len( daily_returns )
    for i in range(1,n_values):
        daily_returns[i] = (na_portfolio[i]/na_portfolio[i-1]) - 1

    daily_ret = np.mean( daily_returns )
    vol = np.std( daily_returns )
    sharpe = daily_ret/vol * math.sqrt(252)

    if(_print_):
        print "Start Date: ", dt_start
        print "End Date: ", dt_end
        print "Symbols: ", ls_symbols
        print "Optimal Allocations: ", weights
        print "Sharpe Ratio: ", sharpe
        print "Volatility (stdev of daily returns): ", vol
        print "Average Daily Return: ", daily_ret
        print "Cumulative Return: ", cum_ret

#todo ->         plt.clf()
#todo ->         plt.plot(ldt_timestamps, na_portfolio)
#todo ->         plt.plot(ldt_timestamps, na_normalized_price)
#todo ->         plt.legend('portfolio')
#todo ->         plt.legend(ls_symbols)
#todo ->         plt.ylabel('Cumulative Daily Returns')
#todo ->         plt.xlabel('Date')
#todo ->         plt.savefig('cum_daily_return_portfolio.pdf', format='pdf')
#todo ->         plt.show()

    # of the total portfolio
    return vol, daily_ret, sharpe, cum_ret

def main():
    ''' Main Function'''

    #1st example
    # Start and End date of the charts
    dt_start = dt.datetime(2011, 1, 1)
    dt_end = dt.datetime(2011, 12, 31)

    # List of symbols
    ls_symbols = ["AAPL", "GLD", "GOOG", "XOM"]

    # Allocation
    weights = [0.4, 0.4, 0.0, 0.2]

    # 2nd example
    dt_start = dt.datetime(2010, 1, 1)
    dt_end = dt.datetime(2010, 12, 31)
    ls_symbols = ["AXP", "HPQ", "IBM", "HNZ"]
    weights = [0.0, 0.0, 0.0, 1.0]

    dt_start = dt.datetime(2011, 1, 1)
    dt_end = dt.datetime(2011, 12, 31)
    ls_symbols =  ["BRCM", "TXN", "IBM", "HNZ"]
    weights = [0.0, 0.0, 0.0, 1.0]

#    simulate(dt_start, dt_end, ls_symbols, weights, True)
#    return

    weights = np.zeros(4)
    increment = 0.1
    total = int(1.0/increment + 0.5)

    vol_max = 0
    daily_ret_max = 0
    sharpe_max = 0
    cum_ret_max = 0
    
    weights_max = np.zeros(4)

    for i in range(0,total+1):
        for j in range(0,total+1):
            for k in range(0,total+1):
                for l in range(0,total+1):
                    sum = (i+j+k+l)
                    if(sum!=total): continue
                    weights [0]=  float(i)
                    weights [1]=  float(j)
                    weights [2]=  float(k)
                    weights [3]=  float(l)
                    weights *= increment
                    #print weights
                    vol, daily_ret, sharpe, cum_ret = simulate(dt_start, dt_end, ls_symbols, weights, False)
                    if(sharpe_max < sharpe):
                        vol_max = vol
                        daily_ret_max = daily_ret
                        sharpe_max = sharpe
                        cum_ret_max = cum_ret
                        weights_max = weights.copy()


    print 'vol = ', vol_max
    print 'daily_ret = ', daily_ret_max
    print 'sharpe = ', sharpe_max
    print 'cum_ret = ', cum_ret_max
    print 'weights = ', weights_max

if __name__ == '__main__':
    main()
