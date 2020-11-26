#close
#When you run this script it will give you all the stocks that were pulled 
#from a screener from IBD stock screener. Save the screened stocks to where it says holdings
#When you run it it saves all the data to ohlc file in a .txt format thats readable by the 
# by the stocks name individaully
#config is a seperate file containing bars url and api keys for headers


from csv import writer
import config, requests, json
from datetime import datetime


holdings = open('data/ccc.csv').readlines()
symbols = [holding.split(',')[0].strip() for holding in holdings][1:185]  # the [0] represents the column you want to pull, and the [1:] at the end represents removing the stocks at the 1 postiiton 
symbols = ",".join(symbols)                                              # ALPACA WANTS THE STOCKS LIKE AA,BA NOT 'AA','BA' REMOVES THE COMA AND PUTS IN A LIST


#day_bars_url = '{}/day?symbols={}&limit=1000'.format(config.BARS_URL, symbols)
minute_bars_url = '{}/15Min?symbols={}&limit=500'.format(config.BARS_URL, symbols)

r = requests.get(minute_bars_url, headers=config.HEADERS)

data = r.json()
#print(r.content)
#print(json.dumps(r.json(), indent=4))
#print(symbols)

for symbol in data:
    filename = 'data/ohlc/{}.txt'.format(symbol)
    f = open(filename, 'w+')
    f.write('Date,Open,High,Low,close,Volume,OpenInterest\n')
    #print(data[symbol])
         
    for bar in data[symbol]:
        t = datetime.fromtimestamp(bar['t'])
        day = t.strftime('%Y-%m-%d')
        line = "{},{},{},{},{},{},{}\n".format(day, bar['o'], bar['h'], bar['l'], bar['c'], bar['v'], 0.00)
        f.write(line)