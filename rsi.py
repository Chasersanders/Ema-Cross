
import alpaca_trade_api as tradeapi
import fxcmpy as fxcmpy
import time
import datetime as dt
from pyti.relative_strength_index import relative_strength_index as rsi


api_key = 'PKEI8HFRZAJRDEZHT310'                                         #Alpaca account API key
api_secret = 'NWAnxnRAnUKKVfOQTKum3RllQOoJv0EPTa8e4LJC'                   # Alpaca account secret key
base_url = 'https://paper-api.alpaca.markets'                             # Alpaca URL
#orders_URL = "{}/v2/orders".format(base_url)                             # Routes to Alpaca order URL
headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret}
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')




symbol = 'EUR/USD'
timeframe = "m15"           # (m1,m5,m15,m30,H1,H2,H3,H4,H6,H8,D1,W1,M1)
rsi_periods = 14
upper_rsi = 70.0
lower_rsi = 30.0
amount = 1
stop = -20
limit = None

# This function places a market order in the direction BuySell, "B" = Buy, "S" = Sell, uses symbol, amount, stop, limit
def enter(BuySell):
    direction = True;
    if BuySell == "S":
        direction = False;
    try:
        opentrade = con.open_trade(symbol=symbol, is_buy=direction,amount=amount, time_in_force='GTC',order_type='AtMarket',is_in_pips=True,limit=limit, stop=stop)
    except:
        print("   Error Opening Trade.")
    else:
        print("   Trade Opened Successfully.")



# This function closes all positions that are in the direction BuySell, "B" = Close All Buy Positions, "S" = Close All Sell Positions, uses symbol
def exit(BuySell=None):
    openpositions = con.get_open_positions(kind='list')
    isbuy = True
    if BuySell == "S":
        isbuy = False
    for position in openpositions:
        if position['currency'] == symbol:
            if BuySell is None or position['isBuy'] == isbuy:
                print("   Closing tradeID: " + position['tradeId'])
                try:
                    closetrade = con.close_trade(trade_id=position['tradeId'], amount=position['amountK'])
                except:
                    print("   Error Closing Trade.")
                else:
                    print("   Trade Closed Successfully.")








# Returns true if stream1 crossed over stream2 in most recent candle, stream2 can be integer/float or data array
def crossesOver(stream1, stream2):
    # If stream2 is an int or float, check if stream1 has crossed over that fixed number
    if isinstance(stream2, int) or isinstance(stream2, float):
        if stream1[len(stream1)-1] <= stream2:
            return False
        else:
            if stream1[len(stream1)-2] > stream2:
                return False
            elif stream1[len(stream1)-2] < stream2:
                return True
            else:
                x = 2
                while stream1[len(stream1)-x] == stream2:
                    x = x + 1
                if stream1[len(stream1)-x] < stream2:
                    return True
                else:
                    return False
    # Check if stream1 has crossed over stream2
    else:
        if stream1[len(stream1)-1] <= stream2[len(stream2)-1]:
            return False
        else:
            if stream1[len(stream1)-2] > stream2[len(stream2)-2]:
                return False
            elif stream1[len(stream1)-2] < stream2[len(stream2)-2]:
                return True
            else:
                x = 2
                while stream1[len(stream1)-x] == stream2[len(stream2)-x]:
                    x = x + 1
                if stream1[len(stream1)-x] < stream2[len(stream2)-x]:
                    return True
                else:
                    return False
# Returns true if stream1 crossed under stream2 in most recent candle, stream2 can be integer/float or data array
def crossesUnder(stream1, stream2):
    # If stream2 is an int or float, check if stream1 has crossed under that fixed number
    if isinstance(stream2, int) or isinstance(stream2, float):
        if stream1[len(stream1)-1] >= stream2:
            return False
        else:
            if stream1[len(stream1)-2] < stream2:
                return False
            elif stream1[len(stream1)-2] > stream2:
                return True
            else:
                x = 2
                while stream1[len(stream1)-x] == stream2:
                    x = x + 1
                if stream1[len(stream1)-x] > stream2:
                    return True
                else:
                    return False
    # Check if stream1 has crossed under stream2
    else:
        if stream1[len(stream1)-1] >= stream2[len(stream2)-1]:
            return False
        else:
            if stream1[len(stream1)-2] < stream2[len(stream2)-2]:
                return False
            elif stream1[len(stream1)-2] > stream2[len(stream2)-2]:
                return True
            else:
                x = 2
                while stream1[len(stream1)-x] == stream2[len(stream2)-x]:
                    x = x + 1
                if stream1[len(stream1)-x] > stream2[len(stream2)-x]:
                    return True
                else:
                    return False








# Returns number of Open Positions for symbol in the direction BuySell, returns total number of both Buy and Sell positions if no direction is specified
def countOpenTrades(BuySell=None):
    openpositions = con.get_open_positions(kind='list')
    isbuy = True
    counter = 0
    if BuySell == "S":
        isbuy = False
    for position in openpositions:
        if position['currency'] == symbol:
            if BuySell is None or position['isBuy'] == isbuy:
                counter+=1
    return counter






# This function is run every time a candle closes
def Update():
    print(str(dt.datetime.now()) + "     " + timeframe + " Bar Closed - Running Update Function...")

    # Calculate Indicators
    iRSI = rsi(pricedata['bidclose'], rsi_periods)

    # Print Price/Indicators
    print("Close Price: " + str(pricedata['bidclose'][len(pricedata)-1]))
    print("RSI: " + str(iRSI[len(iRSI)-1]))

    # TRADING LOGIC

    # Entry Logic
    # If RSI crosses over lower_rsi, Open Buy Trade
    if crossesOver(iRSI, lower_rsi):
        print("   BUY SIGNAL!")
        print("   Opening Buy Trade...")
        enter("B")
    # If RSI crosses under upper_rsi, Open Sell Trade
    if crossesUnder(iRSI, upper_rsi):
        print("   SELL SIGNAL!")
        print("   Opening Sell Trade...")
        enter("S")

    # Exit Logic
    # If RSI is greater than upper_rsi and we have Buy Trade(s), Close Buy Trade(s)
    if iRSI[len(iRSI)-1] > upper_rsi and countOpenTrades("B") > 0:
        print("   RSI above " + str(upper_rsi) + ". Closing Buy Trade(s)...")
        exit("B")
    # If RSI is less than than lower_rsi and we have Sell Trade(s), Close Sell Trade(s)
    if iRSI[len(iRSI)-1] < lower_rsi and countOpenTrades("S") > 0:
        print("   RSI below " + str(lower_rsi) + ". Closing Sell Trade(s)...")
        exit("S")

    print(str(dt.datetime.now()) + "     " + timeframe + " Update Function Completed.\n")