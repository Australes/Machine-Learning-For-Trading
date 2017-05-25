import os
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 

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
 
 def calculate_portfolio_value(normalized_df, start_investment, symbols, allocation_fraction):
    stock_investment = start_investment * allocation_fraction
    stock_values = normalized[symbols] * stock_investment
    portfolio_value = stock_values.sum(axis = 1)
    plot(portfolio_value, 'Portfolio value')
    return portfolio_value


if __name__ == "__main__":
    
    symbols = ['SPY', 'AAPL', 'GOOG', 'IBM', 'TSLA']
    start = '2013-01-01'
    end = '2013-12-31'
    
    dates = dates_creator(start, end)
    df = get_data(symbols, dates)
    # Daily portfolio
    normalized = normalize_data(df)
    
    #portfolio_value = calculate_portfolio_value(normalized, start_investment, symbols, allocation_fraction)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
