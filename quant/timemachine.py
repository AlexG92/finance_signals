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

from datetime import datetime
import quantpredict
import bisect
import copy
import matplotlib.pyplot as grapher
import sys


# Static Data
ticker = 'AMZN'
samplespath = "../samples/%s.csv" % ticker
lines_5yr = 1260
cumulativehistory = []


def jumpto(year, month, day):
    """ Find index of a requested day in historic data """
    d = datetime(year, month, day).date()
    return bisect.bisect_left([row['date'] for row in cumulativehistory], d)


def verifyprediction(stance, price, date, timeperiod=60, method="direction"):
    """
    Determine if the predicted stance is correct.

    If method is direction, prediction for general direction is checked. The average closing price of the following days within the timeperiod limit is compared.

    If method is order, prediction is treated as actual order and expected to be profitable within the timeperiod. Price needs to move at least 5% in the desired direction.

    i.e. a buy order at 100 would look for a high of 105 in the next X (timeperiod) days. A sell order at 100 looks for a low of 95 or less before declaring success.

    In: details of the prediction
        stance of prediction, to buy or sell
        closing price of that day
        date prediction made on
    Out: a number representing percentage movement relative to horizon. Positive is desireable, negative means price movement in opposite to prediction
    """
    today = jumpto(date.year, date.month, date.day)
    window = cumulativehistory[today:today + timeperiod]
    percentage = 0.05
    print("%d price: %d" % (stance, price))

    if stance == 1:  # buy
        prices = [row['h'] for row in window]

        def check(a):
            return price * (1 + percentage) < a

    elif stance == -1:  # sell
        # print("sell stance")
        prices = [row['l'] for row in window]
        # print(price * (1 - percentage))

        def check(a):
            return price * (1 - percentage) > a
    else:
        # Stance zero meaning no action
        pass

    # print(', '.join([str(p) for p in prices]))
    print(list(map(check, prices)))
    print(min(prices))


# Read history

line_counter = 0
with open(samplespath) as file:
    file.readline()  # remove csv header
    for line in file:
        line_counter += 1
        line = line.strip('\n')
        data = line.split(',')
        d = {'date': datetime.strptime(data[0], '%Y-%m-%d').date(),
             'o': round(float(data[1]), 2),
             'h': round(float(data[2]), 2),
             'l': round(float(data[3]), 2),
             'c': round(float(data[4]), 2),
             'vol': int(data[5])}
        cumulativehistory.insert(0, d)

# Debug stuff
# print("read %i lines" % line_counter)
# for x in range(0, 9):
#     print(cumulativehistory[x])
# print(cumulativehistory[200])
# print(cumulativehistory[jumpto(2011, 7, 1)])

# Analyze and make prediction

# Simulate today is july 1, 2011
start = jumpto(2011, 7, 1)  # ensure enough data for 200 SMA
end = line_counter

capital = 10000
profit = 0
holdings = 0

# for x in range(end - 1, end):
#     print("Outlook on day: " + str(cumulativehistory[x]['date']))
#     # snapshot = copy.deepcopy(cumulativehistory[:jumpto(2012, 7, 1) + 1])
#     snapshot = copy.deepcopy(cumulativehistory[:x])
#     q = quantpredict.profile(ticker, snapshot)
#     quantpredict.analyze(q)
#     stance = quantpredict.predict(q)

# print(profit)

print("Outlook on day: " + str(cumulativehistory[start]['date']))
# snapshot = copy.deepcopy(cumulativehistory[:jumpto(2012, 7, 1) + 1])
snapshot = copy.deepcopy(cumulativehistory[:start + 1])
# print(snapshot[len(snapshot) - 1])
q = quantpredict.profile(ticker, snapshot)
quantpredict.analyze(q)
stance = quantpredict.predict(q)
verifyprediction(stance, snapshot[start]['c'], snapshot[start]['date'], method="order")

# Sample plotting

if len(sys.argv) > 1:
    if sys.argv[1] == "--graph":
        # snapshot = copy.deepcopy(cumulativehistory)
        # q = quantpredict.profile(ticker, snapshot)
        # quantpredict.analyze(q)
        # quantpredict.predict(q)
        # print(q.priceplot())
        # grapher.subplot(211)
        grapher.plot(q.getplot('c'))
        grapher.plot(q.getplot('sma'))
        grapher.plot(q.getplot('bb_upper'))
        grapher.plot(q.getplot('bb_middle'))
        grapher.plot(q.getplot('bb_lower'))
        grapher.ylabel('price')

        # grapher.subplot(212)
        # grapher.plot(q.studies['rsi'])
        grapher.show()
    elif sys.argv[1] == "--graph-all":
        snapshot = copy.deepcopy(cumulativehistory)
        q = quantpredict.profile(ticker, snapshot)
        quantpredict.analyze(q)
        quantpredict.predict(q)
        # print(q.priceplot())
        # grapher.subplot(211)
        grapher.plot(q.getplot('c'))
        grapher.plot(q.getplot('sma'))
        grapher.plot(q.getplot('bb_upper'))
        grapher.plot(q.getplot('bb_middle'))
        grapher.plot(q.getplot('bb_lower'))
        grapher.ylabel('price')

        # grapher.subplot(212)
        # grapher.plot(q.studies['rsi'])
        grapher.show()
