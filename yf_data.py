import yfinance as yf

def yf_data(quote = 'AAPL', period = '1mo', interval = '1d'):
    quote = yf.Ticker('quote')
    return quote.history(period=period, interval=interval)