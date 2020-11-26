
import alpaca_trade_api as tradeapi
import requests, json
import pandas as pd
from tabulate import tabulate
import pytz
import datetime as dt
from datetime import date
import numpy as np
import threading
import matplotlib.pyplot as plt


def printit():
    threading.Timer(5.0, printit).start()
#------------------------------------------connecting to the alpaca platform------------#
#authentication and connection details
api_key = 'PKEI8HFRZAJRDEZHT310'                                            #Alpaca account API key
api_secret = 'NWAnxnRAnUKKVfOQTKum3RllQOoJv0EPTa8e4LJC'                     # Alpaca account secret key
base_url = 'https://paper-api.alpaca.markets'                               # Alpaca URL
#orders_URL = "{}/v2/orders".format(base_url)                               # Routes to Alpaca order URL
headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret}


#instantiate REST API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')



def techindicators(
    self, techindicator='SMA', output_format='json', **kwargs):
    ''' Returns one of the technical indicator endpoints of the
    Alpha Vantage API.

    Params:
        techindicator: The technical indicator of choice
        params: Each technical indicator has additional optional parameters

    Returns:
        pandas, csv, or json
    '''
    if output_format:
        self._techindicators.output_format = output_format
    params = {'function': techindicator}
    for key, value in kwargs.items():
        params[key] = value
    data = self.get(params)
    return data



    # Import Matplotlib's `pyplot` module as `plt`


# Plot the closing prices for `aapl`
AAPL['Close'].plot(grid=True)

# Show the plot
plt.show()