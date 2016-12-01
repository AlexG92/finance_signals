import sys
from read_ticker_csv import get_stock_data
from ticker_classes import TickerMetrics

ticker = ""
try:
    ticker = sys.argv[1]
except IndexError:
    raise IndexError("Need to enter valid ticker as a system param.")

ticker_data = TickerMetrics(get_stock_data(ticker))

print ticker_data.get_max()
print ticker_data.get_min()
print ticker_data.get_mean()
print ticker_data.get_variants()
