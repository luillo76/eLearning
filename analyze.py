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

def main(argv):
    initial_cash = float(argv[0])
    orders, ls_symbols, dt_start, dt_end = read_orders(argv[1])
    fname = argv[2]

    d_data = get_symbols_data(ls_symbols, dt_start, dt_end)

    # Getting the numpy ndarray of actual close prices
    na_price = d_data['actual_close']

    na_portfolio = get_portfolio_value(initial_cash, orders, na_price)

    write_portfolio(fname, na_portfolio)
    print_results(dt_start, dt_end)

if __name__ == "__main__":
    main(sys.argv[1:])
