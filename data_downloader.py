import yfinance as yf

stocks = [
    'TSLA', 'AAPL', 'NVDA', 'AMZN', 'MSFT', 'F', 'AMC', 'VOO', 'SPY', 'DIS',
    'SNDL', 'VWO', 'VEA', 'BND', 'META', 'GOOGL', 'NIO', 'VTI', 'IVV', 'AMD',
    'LCID', 'NFLX', 'PLTR', 'SPMO', 'RIVN', 'QQQ', 'PFE', 'GME', 'SNAP', 'KO',
    'PLUG', 'T', 'SOFI', 'XOM', 'BABA', 'ABNB', 'PYPL', 'SQ', 'TQQQ', 'SBUX',
    'V', 'JPM', 'BA', 'COST', 'MARA', 'DKNG', 'MRNA', 'CRSP', 'ARKK', 'TLRY',
    'NKE', 'UBER', 'CCIV', 'ZM', 'ROKU', 'SPCE', 'PINS', 'GM', 'TWTR', 'NVAX',
    'AAL', 'NCLH', 'UAL', 'CCL', 'DAL', 'RBLX', 'FUBO', 'QS', 'BB', 'RIOT',
    'ET', 'WMT', 'CLNE', 'GE', 'NOK', 'SIRI', 'ATVI', 'ENPH', 'DOCU', 'BMY',
    'VZ', 'INTC', 'CSCO', 'PSEC', 'ORCL', 'SLV', 'GLD', 'ARKG', 'ARKF', 'SPHD',
    'SPYD', 'SPYG', 'SPYV', 'SPYW', 'SPYX', 'SPYB', 'SPYC', 'SPYI', 'SPYJ'
]

for stock in stocks:
    work = yf.Ticker(stock)
    history = work.history(period="5y")
    if history.empty:
        continue
    history.to_csv(f"./data/{stock}.csv")