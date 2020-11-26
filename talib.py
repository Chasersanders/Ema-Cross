import btalib
import pandas as pd 

df = pd.read_csv('data/ohlc/SPSC.txt', parse_dates=True, index_col="Date")

sma = btalib.sma(df)
rsi = btalib.rsi(df)
macd = btalib.macd(df)

 
 
#SMA15 = btalib.sma(df, period=15)
#SMA50 = btalib.sma(df, period=50)
#SMA200 = btalib.sma(df, period=200)

#if SMA50 > SMA200:
    

df['sma'] = sma.df         
df['rsi'] = rsi.df      


#macd = ema(data, 12) - ema(data, 26)
#signal = ema(macd, 9)
#histogram = macd - signal

df['macd'] = macd.df['macd']  
df['signal'] = macd.df['signal']
df['histogram'] = macd.df['histogram']






oversold_days = df[df['rsi'] < 30 ]
overbought_days = df[df['rsi'] > 60]
print(oversold_days)
print(overbought_days)

print(df)