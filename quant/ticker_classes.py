from datetime import datetime

class StockDay:
    def __init__(self, line, line_number):
        line = line.strip('\n')
        data = line.split(',')
        
        self.line_number = line_number
        self.day = datetime.strptime(data[0], '%Y-%m-%d').date()
        self.op = round(float(data[1]), 2)
        self.hi = round(float(data[2]), 2)
        self.lo = round(float(data[3]), 2)
        self.cl = round(float(data[4]), 2)
        self.vol = int(data[5])

class TickerMetrics:
    def __init__(self, ticker_data):
        self.ticker_data = ticker_data
        self.length = len(self.ticker_data)

    def get_max(self):
        biggest_stock_value = 0
        for stock_day in self.ticker_data:
            if (stock_day.hi > biggest_stock_value):
                biggest_stock_value = stock_day.hi
        self.max = biggest_stock_value
        return self.max

    def get_min(self):
        lowest_stock_value = ""
        for stock_day in self.ticker_data:
            if (stock_day.lo < lowest_stock_value):
                lowest_stock_value = stock_day.lo
        self.min = lowest_stock_value
        return self.min


    def get_mean(self):
        aggregrate_ticker_close = 0
        for stock_day in self.ticker_data:
            aggregrate_ticker_close += stock_day.cl
        self.mean = aggregrate_ticker_close/self.length
        return self.mean

    def get_variants(self):
        self.get_mean()
        clmn2_total = 0
        for stock_day in self.ticker_data:
            clmn = (stock_day.cl - self.mean)
            clmn2 = clmn * clmn
            clmn2_total += clmn2
        self.variants = clmn2_total/self.length
        return self.variants



