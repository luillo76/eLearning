import sys
import time
import datetime
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import pandas as pd
import numpy as np
#
# check for command line arguments - add manually if not found (Idle doesn't support command line args)
if len(sys.argv) < 2:
    sys.argv = [sys.argv[0], 'BollTradesOpposite.csv']
#
# read the orders file
print 'Reading order data...'
orderData = []
dataFile = open(sys.argv[1] , 'r')
for line in dataFile:
    orderData.append(line.strip('\n'))
dataFile.close
#
# check to make sure there are an even number of records in orders file.  If not it probably means
# a trade is still open at the end of the time period
if len(orderData)%2 <> 0:
    print 'The order file does not have an even number of records - program cannot proceed'
    sys.exit()
#
# read order data and create a list for dates, symbols, and roundtrip trades 
tradeList = []
dateList = []
symList = []
index = 0
while index < len(orderData)-1: #read two records at a time - the opening trade and the exit
    year,month,day,symbol,action,qty,junk = orderData[index].split(',') #junk reads unused data past trade info - may not be needed
    openDate = datetime.datetime(int(year),int(month),int(day),16)
    if action == 'Buy':
        tradeType = 'Long'
    elif action == 'Sell':
        tradeType = 'Short'
    index += 1
    year,month,day,symbol,action,qty,junk = orderData[index].split(',') #junk reads unused data past trade info - may not be needed
    exitDate = datetime.datetime(int(year),int(month),int(day),16)
    tradeList.append([symbol,qty,tradeType,openDate,exitDate])
    dateList.append(openDate)
    dateList.append(exitDate)
    if symbol not in symList: symList.append(symbol)
    index += 1
dateList=sorted(dateList)
startDate = dateList[0]
endDate = dateList[-1]
#
# get pricing data for symbols over the date interval required
print 'Getting price data...'
timeofday = datetime.timedelta(hours=16)
timestamps = du.getNYSEdays(startDate, endDate, timeofday)
c_dataobj = da.DataAccess('Yahoo')
ls_keys = ['close']
ldf_data = c_dataobj.get_data(timestamps, symList, ls_keys)
d_data = dict(zip(ls_keys, ldf_data))
for s_key in ls_keys:
    d_data[s_key] = d_data[s_key].fillna(method='ffill')
    d_data[s_key] = d_data[s_key].fillna(method='bfill')
    d_data[s_key] = d_data[s_key].fillna(1.0)
priceData = d_data['close']
#
# analyze each trade
print 'Analyzing trade data...'
winList = []
loseList = []
for trade in tradeList:
    symbol = trade[0]
    qty = trade[1]
    tradeType = trade[2]
    openDate = trade[3]
    openDateTS = pd.DatetimeIndex([trade[3]])[0]#convert datetime to timestamp    
    exitDateTS = pd.DatetimeIndex([trade[4]])[0]
    profit = ((priceData[symbol][exitDateTS]/priceData[symbol][openDateTS])-1)*100
    if tradeType == 'Short': profit = -1.0*profit
    if profit >= 0.0 : winList.append(profit)
    else: loseList.append(profit)
#
print 'Compiling trade stats...'
roundTrips = float(len(winList)+len(loseList))
print
print 'Trade Statistics for file ' + sys.argv[1]
print
print 'Date range ' + str(startDate) + ' to ' + str(endDate)
print
print 'Number of roundtrip trades: %d' % (int(roundTrips))
print 'Percent winners: %.1f \tPercent losers: %.1f' % (100*len(winList)/roundTrips,100*len(loseList)/roundTrips)
print 'Average Win: %.2f \tAverage Loss: %.2f' % (np.mean(winList),np.mean(loseList))
print 'Biggest Win: %.2f \tBiggest Loss: %.2f' % (np.max(winList),np.min(loseList))
