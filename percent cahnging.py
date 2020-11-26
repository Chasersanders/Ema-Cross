import alpaca_trade_api as tradeapi
import requests, json
import pandas as pd
from tabulate import tabulate
import pytz
import datetime as dt
from datetime import datetime, timedelta
import numpy as np
import talib

#authentication and connection details
api_key = 'PK8GLY3IT3YTLC6I2B7E'                                         #Alpaca account API key
api_secret = 'XMu9xQp28wvtULlmiVBSl2o3Uo8jijF9gBPisTJ3'                   # Alpaca account secret key
base_url = 'https://paper-api.alpaca.markets'                             # Alpaca URL
orders_URL = "{}/v2/orders".format(base_url)                             # Routes to Alpaca order URL
headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret}

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')



def run_live(api):
    cycle = 0 # Only used to print a "waiting" message every few minutes.

    # See if we've already bought or sold positions today. If so, we don't want to do it again.
    # Useful in case the script is restarted during market hours.
    bought_today = False
    sold_today = False
    try:
        # The max stocks_to_hold is 200, so we shouldn't see more than 400
        # orders on a given day.
        orders = api.list_orders(
            after=api.format(datetime.today() - timedelta(days=1)),
            limit=400,
            status='all'
        )
        for order in orders:
            if order.side == 'buy':
                bought_today = True
                # This handles an edge case where the script is restarted
                # right before the market closes.
                sold_today = True
                break
            else:
                sold_today = True
    except:
        # We don't have any orders, so we've obviously not done anything today.
        pass

    while True:
        # We'll wait until the market's open to do anything.
        clock = api.get_clock()
        if clock.is_open and not bought_today:
            if sold_today:
                # Wait to buy
                time_until_close = clock.next_close - clock.timestamp
                # We'll buy our shares a couple minutes before market close.
                if time_until_close.seconds <= 120:
                    print('Buying positions...')
                    portfolio_cash = float(api.get_account().cash)
                    ratings = api.get_ratings(
                        api, None
                    )
                    shares_to_buy = api.get_shares_to_buy(ratings, portfolio_cash)
                    for symbol in shares_to_buy:
                        api.submit_order(
                            symbol=symbol,
                            qty=shares_to_buy[symbol],
                            side='buy',
                            type='market',
                            time_in_force='day'
                        )
                    print('Positions bought.')
                    bought_today = True
            else:
                # We need to sell our old positions before buying new ones.
                time_after_open = clock.next_open - clock.timestamp
                # We'll sell our shares just a minute after the market opens.
                if time_after_open.seconds >= 60:
                    print('Liquidating positions.')
                    api.close_all_positions()
                sold_today = True
        else:
            bought_today = False
            sold_today = False
            if cycle % 10 == 0:
                print("Waiting for next market day...")
        time.sleep(30)
        cycle+=1
		
			
		
