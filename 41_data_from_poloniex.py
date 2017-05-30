from poloniex import Poloniex

connection = Poloniex()
BTC_ETH = connection.returnTicker()

print(type(BTC_ETH))
print(BTC_ETH.keys())