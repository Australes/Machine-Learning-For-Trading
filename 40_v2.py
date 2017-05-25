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

def find_portfolio_statistics(allocs, df, gen_plot):
    dfcopy = df.copy()
    
    	# Find cumulative value over time
    df = (df/df.iloc[0])
    df = df * allocs
    df = df.sum(axis=1)
    
    # Compute Portfolio Statistics
    cumulative_return = (df.iloc[-1]/df.iloc[0]) - 1
    dailyreturns = (df.iloc[1:]/df.iloc[:-1].values) - 1
    average_daily_return = dailyreturns.mean(axis = 0)
    std_daily_return = dailyreturns.std(axis = 0)
    sharpe_ratio = (252 ** (1/2.0)) * ((average_daily_return - 0) / std_daily_return)
    ending_value = df.iloc[-1]
    total_returns = average_daily_return*(252/252)
    
    #Plot portfolio along SPY
    dfcopynormed = dfcopy['SPY']/dfcopy['SPY'].iloc[0]
    ax = dfcopynormed.plot(title = 'Daily Portfolio Value and SPY', label = 'SPY')
    sumcopy = dfcopy.sum(axis = 1)
    normed = sumcopy/sumcopy.iloc[0]
    normed.plot(label='Portfolio Value', ax = ax)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend(loc = 2)
    plt.show()
     
    return (-1 * sharpe_ratio)

	
        

if __name__ == "__main__":
    
    symbols = ['SPY', 'AAPL', 'GOOG', 'TSLA']
    allocs = [0.0, 0.5, 0.35, 0.15]
    start = '2013-01-01'
    end = '2013-12-31'
    start_investment = 100
    
    num_stocks = len(symbols)
    allocation_fraction = np.ones(num_stocks) / num_stocks
    
    
    dates = dates_creator(start, end)
    df = get_data(symbols, dates)
    
    
    
    annualized_sharpe_ratio = find_portfolio_statistics(allocs, df, gen_plot = True)
    
    print('Annualized Sharpe ratio:')
    print(annualized_sharpe_ratio)
    
    
    
    
    
    
    
    
    
    
    
    