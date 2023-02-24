import yfinance as yf
from pymongo import MongoClient
import pandas as pd

def finance_data(quote='AAPL', interval = '1d'):
    # Récupération des données sur un an 
    quote = yf.Ticker(quote)
    hist = quote.history(period='1y', interval=interval)
    hist.drop(['Dividends','Stock Splits'], axis = 1, inplace = True)
    hist = hist.reset_index()
    
    date=[]
    for i in hist['Date']:
        date.append(i.date())
    hist['Date']=date
    
    # Récupération des données sur le dernier mois
    hist_analyse = quote.history(period='1mo', interval=interval)
    hist_analyse.drop(['Dividends','Stock Splits'], axis = 1, inplace = True)
    hist_analyse = hist_analyse.reset_index()
    
    date_temp = []
    avg = []
    for i in range(len(hist_analyse)):
        date_temp.append(hist_analyse['Date'][i].date())
        avg.append((hist_analyse['High'][i]+hist_analyse['Low'][i])/2)
    hist_analyse['Avg'] = avg
    
    var = []
    for i in hist_analyse['Avg']:
        var.append(((i/(hist_analyse['Avg'].sum()/hist_analyse.shape[0]))-1)*100)
        
    hist_analyse['Var'] = (var)
    return hist, hist_analyse
