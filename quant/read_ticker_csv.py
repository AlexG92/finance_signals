# import csv
# Get Ticker From System Param.

from ticker_classes import StockDay

def get_stock_data(ticker):
    # Static Data
    csv = "../samples/%s.csv" % ticker
    lines_5yr = 1260
    stock_day_list = []

    line_counter = 0
    with open(csv) as file:
        file.readline()  # remove csv header
        for line in file:
            line_counter += 1
            stock_day_list.append(StockDay(line, line_counter))

    return stock_day_list