import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm


def timestamp2date(timestamp):
    # function converts a Uniloc timestamp into Gregorian date
    return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')

def date2timestamp(date):
    # function coverts Gregorian date in a given format to timestamp
    return datetime.strptime(date, '%Y-%m-%d').timestamp()


def fetchCryptoOHLC(fsym, tsym):
    # function fetches a crypto price-series for fsym/tsym and stores
    # it in pandas DataFrame

    cols = ['date', 'timestamp', 'open', 'high', 'low', 'close']
    lst = ['time', 'open', 'high', 'low', 'close']

    timestamp_today = datetime.today().timestamp()
    curr_timestamp = timestamp_today

    for j in range(2):
        df = pd.DataFrame(columns=cols)
        # (limit-1) * 2 = days
        # One year is around 184
        limit = 184 
        url = "https://min-api.cryptocompare.com/data/histoday?fsym=" + fsym + "&tsym=" + tsym + "&toTs=" + str(int(curr_timestamp)) + "&limit=" + str(limit)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        dic = json.loads(soup.prettify())
        for i in range(1, limit):
            tmp = []
            for e in enumerate(lst):
                x = e[0]
                y = dic['Data'][i][e[1]]
                if(x == 0):
                    tmp.append(str(timestamp2date(y)))
                tmp.append(y)
            if(np.sum(tmp[-4::]) > 0):
                df.loc[len(df)] = np.array(tmp)
        df.index = pd.to_datetime(df.date)
        df.drop('date', axis=1, inplace=True)
        curr_timestamp = int(df.iloc[0][0])
        if(j == 0):
            df0 = df.copy()
        else:
            data = pd.concat([df, df0], axis=0)

    return data
    
def normalize_data(df):
	return df / df.loc[df.index[0]]

symbols = ['ETH', 'LTC', 'ETC', 'DOGE', 'DGB', 'SC']
#symbols = ['SC']

# Intializing an empty DataFrame
data = pd.DataFrame()

# Adding columns with data for all requested cryptocurrencies
for symbol in tqdm(symbols):
    fsym = symbol
    tsym = "BTC"
    data_symbol = fetchCryptoOHLC(fsym, tsym)
        
    data = pd.concat([data, data_symbol['close']], axis = 1)
    
# Assinging correct names to the columns
data.columns = symbols
# Normalizing the data

#plt.figure(figsize=(12, 4))
for symbol in symbols:
    plt.plot(data[symbol])
plt.ylabel('Cyrrency / BTC', fontsize=12)
plt.legend(loc=2)
plt.show()
'''
open_price = data['open']
high_price = data['high']
low_price = data['low']
close_price = data['close']
'''