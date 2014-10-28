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

def read_symbols(dt_start, dt_end, ls_symbols):

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

    return d_data

def compute_bollinger(dataframe):

    for sym in dataframe.columns:
        df = pd.DataFrame( {'value' : dataframe[sym].values.ravel()}, index=dataframe.index )
        df['rollmean']  = pd.stats.moments.rolling_mean(df['value'].values,20)
        df['rollstd']   = pd.stats.moments.rolling_std (df['value'].values,20)
        df['bollinger'] = (df['value'] - df['rollmean'])/df['rollstd']

        print df.tail()
        plot_bollinger(sym, df)
                                                           
def plot_bollinger(sym, dataframe):
    plt.clf()

    plt.subplot(2, 1, 1)
    plt.plot(dataframe.index, dataframe['value'].values)
    plt.plot(dataframe.index, dataframe['rollmean'].values)
    plt.ylabel('Adjusted close')
    plt.xlabel('Date')
    plt.legend(sym)
    plt.legend('Moving mean')
    
    plt.subplot(2, 1, 2)
    plt.plot(dataframe.index, dataframe['bollinger'].values)
    plt.ylabel('Bollinger')

    fname=sym+'.pdf'
    plt.savefig(fname, format='pdf')
    return

def main():
    ''' Main Function'''

    # Start and End date of the charts
    dt_start = dt.datetime(2010, 1, 1)
    dt_end = dt.datetime(2010, 12, 31)

    # List of symbols
    ls_symbols = ["AAPL", "GOOG", "IBM", "MSFT"]

    d_data = read_symbols(dt_start, dt_end, ls_symbols)

    # Getting the DataFrame of close prices.
    df = d_data['close']
    
    
    compute_bollinger(df)

    return

if __name__ == '__main__':
    main()
