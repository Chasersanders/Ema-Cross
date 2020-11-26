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
api = tradeapi.REST(key_id='PK5IZVQ89X3BUBWSP1JC',secret_key='dyYUFtBdNicjfL8oRg9ht4mYoyI3IbLptus3qgH0')

rate = '1D'                                                  # 1Min, 5Min, 15Min, 1H, 1D
assetsToTrade = ['NFLX']
positionSizing = 0.25

# Tracks position in list of symbols to download
iteratorPos = 0 
assetListLen = len(assetsToTrade)

while iteratorPos < assetListLen:
	symbol = assetsToTrade[iteratorPos],
	
	data = api.get_barset(symbols= symbol, timeframe= '1D', limit = '1000').df
	
	timeList = []
	openList = []
	highList = []
	lowList = []
	closeList = []
	volumeList = []

	# Reads, formats and stores the new bars

	
	# Processes all data into numpy arrays for use by talib
	timeList = np.array(timeList)
	openList = np.array(openList,dtype=np.float64)
	highList = np.array(highList,dtype=np.float64)
	lowList = np.array(lowList,dtype=np.float64)
	closeList = np.array(closeList,dtype=np.float64)
	volumeList = np.array(volumeList,dtype=np.float64)

	# Calculated trading indicators
	SMA20 = talib.sma(closeList,20)
	SMA50 = talib.sma(closeList,50)

	
	# Calculates the trading signals
	if SMA20 > SMA50:
		openPosition = api.get_position(symbol)
		
		# Opens new position if one does not exist
		if openPosition == 0:
			cashBalance = api.get_account().cash
		
			#targetPositionSize = (('cashBalance' / ('price' / 'positionSizing')) # Calculates required position size
			
			order= api.submit_order(symbol,1,"buy","market","gtc") # Market order to open position
			print(order)
		
	else:
		# Closes position if SMA20 is below SMA50
		openPosition = api.get_position(symbol)
		
		returned = api.submit_order(symbol,openPosition,"sell","market","gtc") # Market order to fully close position
		print(returned)
	
	iteratorPos += 1

