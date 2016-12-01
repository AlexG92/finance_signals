#!/usr/bin/python3
"""
Time Machine
Uses historical data to go back in time, and feeds quantpredict data that was available at that time. Use to compare with actual stock movement and check the performace of quantpredict.

In:
csv of ticker

Out:
historical prediction
accuracy of prediction
"""
import sys
from datetime import datetime
import quantpredict
import bisect
import copy
from ticker_classes import StockDay
from read_ticker_csv import get_stock_data

ticker = ""
try:
    ticker = sys.argv[1]
except IndexError:
    raise IndexError("Need to enter valid ticker as a system param.")

#Static Data
history = []


def jumpTo(year, month, day):
    """ Find index of a requested day in historic data """
    d = datetime(year, month, day).date()
    return bisect.bisect_left([row[0] for row in history], d)


# Read history

# Consider using dictionary if it helps with quantpredict so you don't need indexes all the time or something
# https://docs.python.org/3/library/csv.html
stock_data = get_stock_data(ticker)

for stock_day in stock_data:
        history.insert(0, (stock_day.day, stock_day.op, stock_day.hi, stock_day.lo, stock_day.cl, stock_day.vol))

# Debug stuff
# print("read %i lines" % line_counter)
# for x in range(1, 10):
#     print(history[x])
# print(history[200])
# print(history[jumpTo(2011, 7, 1)])

# Analyze and make prediction

snapshot = copy.deepcopy(history[:jumpTo(2011, 7, 1)])

# Consider doing some OOP goodness with this:
# q = quantpredict(snapshot)
# q.analyze()
# q.predict()
# or something
quantpredict.analyze(snapshot)