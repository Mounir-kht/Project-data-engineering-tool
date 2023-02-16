import yfinance as yf
from pymongo import MongoClient
import pandas as pd
def yf_data(quote = 'AAPL', period = '1mo', interval = '1d'):
    quote = yf.Ticker('quote')
    hist = quote.history(period=period, interval=interval)
    hist.drop(['Dividends','Stock Splits'], axis = 1, inplace = True)
    
    client = MongoClient('mongo')
    db = client["reddit_db"]
    yf = db["yahoo_finance"]
    yf.insert_many(hist.to_dict('records'))
    return 
