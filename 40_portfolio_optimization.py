import os
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 

''' Read: http://pandas.pydata.org/pandas-docs/stable/api.html#api-dataframe-stats '''

def symbol_to_path(symbol, base_dir = 'data'):
	return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def dates_creator(start_date, end_date):
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
	return df / df.iloc[0,:]

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
	daily_returns.iloc[0, :] = 0
	return daily_returns
 
def annualised_sharpe(returns, N=252):
    """
    Calculate the annualised Sharpe ratio of a returns stream 
    based on a number of trading periods, N. N defaults to 252,
    which then assumes a stream of daily returns.
    
    The function assumes that the returns are the excess of 
    those compared to a benchmark.
    """
    return np.sqrt(N) * returns.mean() / returns.std()

def calculate_portfolio_value(normalized_df, start_investment, symbols, allocation_fraction):
    stock_investment = start_investment * allocation_fraction
    stock_values = normalized[symbols] * stock_investment
    portfolio_value = stock_values.sum(axis = 1)
    plot(portfolio_value, 'Portfolio value')
    return portfolio_value
    
def annualised_sharpe(returns, N=252):
    """
    Calculate the annualised Sharpe ratio of a returns stream 
    based on a number of trading periods, N. N defaults to 252,
    which then assumes a stream of daily returns.
    
    The function assumes that the returns are the excess of 
    those compared to a benchmark.
    """
    return np.sqrt(N) * returns.mean() / returns.std()
        

if __name__ == "__main__":
    
    symbols = ['SPY', 'AAPL', 'GOOG', 'IBM', 'TSLA']
    start = '2013-01-01'
    end = '2013-12-31'
    start_investment = 100
    
    num_stocks = len(symbols)
    allocation_fraction = np.ones(num_stocks) / num_stocks
    
    
    dates = dates_creator(start, end)
    df = get_data(symbols, dates)
    # Daily portfolio
    normalized = normalize_data(df)
    # Calculating value of the portfolio
    portfolio_value = calculate_portfolio_value(normalized, start_investment, symbols, allocation_fraction)
    
    daily_returns = get_daily_returns(portfolio_value)
    # Sharpe ratio
    annualized_sharpe_ratio = annualised_sharpe(daily_returns, N=252)
    
    print('Annualized Sharpe ratio:')
    print(annualized_sharpe_ratio)
    
    
    
    
    
    
    
    
    
    
    
    
    
    