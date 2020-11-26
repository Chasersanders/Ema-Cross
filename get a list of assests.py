import alpaca_trade_api as tradeapi

api_key = 'PKH38J532Q5MZ87V30RG'                                         #Alpaca account API key
api_secret = 'a90fxhbUixaTjThyZ0DNp8WagePs3T9pwQX9oyTr'                   # Alpaca account secret key
base_url = 'https://paper-api.alpaca.markets'                             # Alpaca URL
#orders_URL = "{}/v2/orders".format(base_url)     
headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret}

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# Get a list of all active assets.
active_assets = api.list_assets(status='active')

# Filter the assets down to just those on NASDAQ.
nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ']
#print(nasdaq_assets)


from time import sleep
import pandas as pd

df = pd.DataFrame(columns=['date', 'price'])

while True:
    try:
        price = api.get_last_quote('V')
        # assigning price to first (and only) item of list and converting from str to float
        mastercard_price = float(price[0])
        
        df.loc[len(df)] = [pd.Timestamp.now(), mastercard_price]
        
        start_time = df.date.iloc[-1] - pd.Timedelta(minutes=60)
        df = df.loc[df.date >= start_time] # cuts dataframe to only include last hour of data
        max_price = df.price.max()
        min_price = df.price.min()
        
        if df.price.iloc[-1] < max_price * 0.99:
            try:
                api.submit_order('V', 500)
                print("DROPPED 1%, CURRENT PRICE: {} MAX PRICE: {}".format(df.price.iloc[-1], max_price))
                break
                
            except Exception as e:
                print("Error placing order:", e)
                
        elif df.price.iloc[-1] > min_price * 1.01:
            try:
                api.order_sell_fractional_by_price('V', 500)
                print("RISEN 1%, CURRENT PRICE: {} MIN PRICE: {}".format(df.price.iloc[-1], min_price))
                break
                
            except Exception as e:
                print("Error placing order:", e)
        
        else:
            print("NO ORDER, CURRENT PRICE: {} MIN PRICE: {} MAX PRICE: {}\n".format(df.price.iloc[-1], min_price, max_price))
            sleep(60)
                
    except Exception as e:
        print("Error fetching latest price:", e)
        
print("ORDER TRIGGERED at {}".format(pd.Timestamp.now()))