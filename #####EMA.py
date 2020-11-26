#####EMA


import alpaca_trade_api as tradeapi
from pytz import timezone
import time

import datetime
#mport config

easterntz = timezone('US/Eastern')

api_key = 'PKH38J532Q5MZ87V30RG'                                         #Alpaca account API key
api_secret = 'a90fxhbUixaTjThyZ0DNp8WagePs3T9pwQX9oyTr'                   # Alpaca account secret key
base_url = 'https://paper-api.alpaca.markets'                             # Alpaca URL
orders_URL = "{}/v2/orders".format(base_url)     
headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret}

def main():
  
  
    # while True:
    #     clock = api.get_clock()
    #     now = clock.timestamp
    #     if clock.is_open:
    #         Universe = universe.Universe
    #         price_df = prices(Universe)
    #         print(price_df[0:200])
    #         # orders = get_order(api, price_df)
    #         # trade(orders)
    #     time.sleep(1)
    #     print("We are about to run again until market is open")

    def prices(symbols):
        now = datetime.datetime.now(easterntz)
        return _get_prices(symbols, now)

def _get_prices(symbols, now, max_workers=5):
    start_dt = (now - datetime.timedelta(50)).isoformat()
    def get_barset(symbols):
        return api.get_barset(
            symbols,
            'day',
            limit = 50,
            start = start_dt,
            end = now
        )
    barset = None
    idx = 0

    print(len(symbols))
    while idx <= len(symbols) - 1:
        if barset is None:
            barset = get_barset(symbols[idx:idx+200])
        else:
            barset.update(get_barset(symbols[idx:idx+200]))
        idx += 200
    return barset.df

def calc_scores(price_df, dayindex=-1):
    diffs = {}
    param = 10
    for symbol in price_df.columns.levels[0]:
        df = price_df[symbol]
        if len(df.close.values):
            continue
        ema = df.close.ewm(span=param).mean()[dayindex]
        last = df.close.values[dayindex]
        diff = (last - ema) / last
        diffs[symbol] = diff
    return sorted(diffs.items(), key=lambda x: x[1])

def get_orders(api, price_df, position_size=100, max_positions=5):
    ranked = calc_scores(price_df)
    to_buy = set()
    to_sell = set()
    account = api.get_account()

    for symbol, _ in ranked[:len(ranked) // 20]:
        price = float(price_df[symbol].close.values[-1])
        if price > float(account.cash):
            continue
        to_buy.add(symbol)
    
    positions = api.list_positions()
    holdings = {p.symbol: p for p in positions}
    holding_symbol = set(holdings.keys())
    to_sell = holding_symbol - to_buy
    to_buy = to_buy - holding_symbol
    orders = []

    for symbol in to_sell:
        shares = holdings[symbol].qty
        orders.append({
            'symbol': symbol,
            'qty': shares,
            'side': 'sell',
        })
    
    max_to_buy = max_positions - (len(positions) - len(to_sell))
    for symbol in to_buy:
        if max_to_buy <= 0:
            break
        shares = position_size // float(price_df[symbol].close.values[-1])
        if shares ==0.0:
            continue
        orders.append({
            'symbol': symbol,
            'qty': shares,
            'side': 'buy',
        })
        max_to_buy -= 1
    return orders

def trade(orders, wait=30):
    sells = [o for o in orders if o['side'] == 'sell']
    for order in sells:
        try:
            api.submit_order(
                symbol=order['symbol'],
                qty=order['qty'],
                side='sell',
                type='market',
                time_in_force='day',
            )
        except Exception as e:
            print(e)
    count = wait
    while count > 0:
        pending = api.list_orders()
        if len(pending) == 0:
            break

        time.sleep(1)
        count -= 1
    
    buys = [o for o in orders if o['side'] == 'buy']
    for order in buys:
        try:
            api.submit_order(
                symbol=order['symbol'],
                qty=order['qty'],
                side='buy',
                type='market',
                time_in_force='day',
            )
        except Exception as e:
            print(e)
    count = wait
    while count > 0:
        pending = api.list_orders()
        if len(pending) == 0:
            break
        time.sleep(1)
        count -= 1

if __name__== '__main__':
    main()