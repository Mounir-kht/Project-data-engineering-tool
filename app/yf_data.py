import yfinance as yf
from pymongo import MongoClient
import pandas as pd

def finance_data(quote='AAPL', period = '1mo', interval = '1d'):
    quote = yf.Ticker(quote)
    hist = quote.history(period=period, interval=interval)
    hist.drop(['Dividends','Stock Splits'], axis = 1, inplace = True)
    client = MongoClient('mongo')
    db = client["reddit_db"]
    yf_db = db["yahoo_finance"]
    
    yf_db.delete_many({}) 
    yf_db.insert_many(hist.to_dict('records'))
    cur = yf_db.find()
    
    date_temp = hist.index
    date=[]
    avg = []
    for i in range(len(date_temp)):
        date.append(date_temp[i].date())
        avg.append((cur[i]['High']+cur[i]['Low'])/2)
        
    df = pd.DataFrame(zip(date,avg),columns=['Date','Avg'])
    
    var = []
    for i in df['Avg']:
        var.append(((i/(df['Avg'].sum()/df.shape[0]))-1)*100)
        
    df['Var'] = (var)
    return df
