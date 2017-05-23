import pandas as pd
import datetime
from pandas_datareader import data

tickers = ['AAPL', 'SPY' , 'IBM', 'GOOG', 'TSLA', 'FB']

for ticker in tickers:
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365*10.0)
    df = data.get_data_yahoo(ticker, start = start_date, end = end_date, interval='d')
    df.to_csv("{}.csv".format(ticker))