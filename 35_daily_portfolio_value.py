import os
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 

''' Read: http://pandas.pydata.org/pandas-docs/stable/api.html#api-dataframe-stats '''

def symbol_to_path(symbol, base_dir = 'data'):
	return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def dates_creator():
	start_date = '2013-01-01'
	end_date = '2013-12-31'
	dates = pd.date_range(start_date, end_date)
	return dates

def get_data(symbols, dates):
	df = pd.DataFrame(index = dates)
	if 'SPY' not in symbols: # adding SPY as the main reference
		symbols.insert(0, 'SPY')
	for symbol in symbols:
		df_temp = pd.read_csv(symbol_to_path(symbol),
			index_col = 'Date',
			parse_dates = True,
			usecols = ['Date', 'Adj Close'],
			na_values = ['nan'])
		df_temp = df_temp.rename(columns = {'Adj Close': symbol})
		df = df.join(df_temp)
	
		if symbol == 'SPY':
			df = df.dropna(subset = ['SPY'])
	return df

def normalize_data(df):
	return df / df.ix[0,:]

def plot(df, title):
	ax = df.plot(title = title, fontsize = 12)
	ax.set_xlabel('Date')
	ax.set_ylabel(title)
	plt.show()

def get_daily_returns(df):
	daily_returns = df.copy()
	# Calculating daily returns
	daily_returns[1:] = (df / df.shift(1)) - 1 
	# Setting daily returns for row 0 to 0.
	daily_returns.ix[0, :] = 0
	return daily_returns

def calculate_portfolio_value(normalized_df, start_investment, symbols, allocation_fraction):
        stock_investment = start_investment * allocation_fraction
        stock_values = normalized[symbols] * stock_investment
        portfolio_value = stock_values.sum(axis = 1)
        plot(portfolio_value, 'Portfolio value')

if __name__ == "__main__":
    '''
    *********************************************************************************************
    Daily portfolio
    price -> price normalized -> resources allocated -> stock value -> portfolio value

    1) Obtaining prices
    2) Normalizing the prices
    price_normalized = price / price[0]
    3) Allocating the resources 
    allocated = price_normalized * allocation_fraction
    where:
    allocation_fraction is 0.1 if you invest 10% of your money in a stock
    4) Stock value
    For all stocks in your portfolio:
    stock_investment = allocated * start_investment
    Stock_value = normalized * stock_investment
    5) Portfolio value
    portfolio_value = stock_value1 + stock_value2 + stock_value3 ...
    In Python:
    portfolio_value = stock_value.sum(axis = 1)
    where:
    .sum(axis = 1) means 'sum all the columns '
    *********************************************************************************************
    '''
    symbols = ['SPY', 'AAPL', 'GOOG', 'IBM']
    allocation_fraction = [0.1, 0.3, 0.4, 0.2]
    dates = dates_creator()
    df = get_data(symbols, dates)
    # Daily portfolio
    start_investment = 1e6 # in USD
    normalized = normalize_data(df)
    
    allocation_fraction = np.array([0.1, 0.3, 0.4, 0.2])
    start_investment = 1e6 # in USD
    
    calculate_portfolio_value(normalized, start_investment, symbols, allocation_fraction)