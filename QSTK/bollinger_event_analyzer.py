'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on January, 23, 2013

@author: Sourabh Bajaj
@contact: sourabhbajaj@gatech.edu
@summary: Event Profiler Tutorial
'''


import pandas as pd
import numpy as np
import math
import copy
import csv
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""

def compute_bollinger(ndarr):

    rollmean  = pd.stats.moments.rolling_mean(ndarr,20)
    rollstd   = pd.stats.moments.rolling_std (ndarr,20)
    bollinger = (ndarr - rollmean)/rollstd

    return bollinger

def find_events(ls_symbols, d_data):
    ''' Finding the event dataframe '''
    df_close = d_data['close']
    ts_market = df_close['SPY']

    bollinger_market = compute_bollinger(ts_market)

    j = 0
    for bol in bollinger_market:
        j += 1
        if( math.isnan(bol) == False): break

    print "Finding Events", j

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    nevents = 0
    orders = []
    for s_sym in ls_symbols:
        bollinger_sym = compute_bollinger(df_close[s_sym])
        for i in range(j, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            f_marketprice_today = ts_market.ix[ldt_timestamps[i]]
            f_marketprice_yest = ts_market.ix[ldt_timestamps[i - 1]]
            f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
            f_marketreturn_today = (f_marketprice_today / f_marketprice_yest) - 1

            f_sym_bollinger_today    = bollinger_sym[i]
            f_sym_bollinger_yest     = bollinger_sym[i - 1]
            f_market_bollinger_today = bollinger_market[i]
            f_market_bollinger_yest  = bollinger_market[i - 1]

            # Event is found if
            if( f_sym_bollinger_today    <= -2.0 and
                f_sym_bollinger_yest     >= -2.0 and
                f_market_bollinger_today >= 1.0) :
                df_events[s_sym].ix[ldt_timestamps[i]] = 1
                nevents += 1
                #buy
                orders.append( [ldt_timestamps[i], 'Buy', s_sym] )
                #sell
                i_sell = i+5
                if(i_sell >= len(ldt_timestamps)):
                    i_sell = len(ldt_timestamps)-1
                orders.append( [ldt_timestamps[i_sell], 'Sell', s_sym])

    print nevents
    return df_events,orders

def write_orders(file_path, orders):

    with open(file_path, mode='w') as file:
        csv_writer = csv.writer(file)

        for i in range(0,len(orders)):
            date = orders[i][0]
            year = date.year
            month = date.month
            day = date.day
            type = orders[i][1]
            sym = orders[i][2]
            
            row_to_enter = [year,month,day,sym,type,100]
            csv_writer.writerow(row_to_enter)

    return

def read_symbols():
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')

    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_events,orders = find_events(ls_symbols, d_data)
    write_orders('orders.csv', orders)
    return df_events,d_data

if __name__ == '__main__':
    df_events,d_data = read_symbols()
    print "Creating Study"
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                     s_filename='MyEventStudy_sp5002008_bollinger.pdf',
                     b_market_neutral=True, b_errorbars=True,
                     s_market_sym='SPY')
