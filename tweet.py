#DISCLAIMER: 
#This example is purely for research illustrative purposes only. 
#Past performance is not indicative of future results. 
#Please DO NOT put any money into this strategy.

#The alpaca paper trading mechanism in this script was copied and modified from the Alpaca Sample Algo - 5 Minute EMA Crossover
#The original code for the 5 Minute EMA Crossover script by Sam Chakerian can be found here: https://gist.github.com/samchaaa/91dfe2bb3c030321536f9799bb369b26

#Import necessary packages
import tweepy
import textblob
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import alpaca_trade_api as tradeapi
import time
import datetime
from datetime import timedelta
from pytz import timezone
import logging

#Setup logging
logging.basicConfig(filename='./vader_sentiment_trader.log', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('{} logging started'.format(datetime.datetime.now().strftime("%x %X")))

#Configure twitter and alpaca API
tz = timezone('EST')


twitter_api_key = 'glUPYlZBf7FoGhuRuKifiRBvn'
twitter_api_secret = 'H1NtkGtoBxRXPSi4NMPIlaj2LzUWPlOrEs1VOiRqExC3pEXiIb'
twitter_access_token = '1161791445826711552-tIB0x2xaC2oQ50BFiGyOoOjuTbeaZG'
twitter_token_secret = 'n6wXQHpsCtO0U6WOFPQ5ewbLFY0m2rpmvU07uCIKR8fh1'
twitter_auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
twitter_auth.set_access_token(twitter_access_token, twitter_token_secret)

api_key = 'PKH38J532Q5MZ87V30RG'                                         #Alpaca account API key
api_secret = 'a90fxhbUixaTjThyZ0DNp8WagePs3T9pwQX9oyTr'                   # Alpaca account secret key
base_url = 'https://paper-api.alpaca.markets'                             # Alpaca URL
orders_URL = "{}/v2/orders".format(base_url)     
headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret}

alpaca_api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')


#Evaluate the sentiment of a given set of ticker symbols
#The default number of tweets to analyze is set at 1000
#When deciding the number of tweets to fetch for each call, consider reviewing the twitter API rate limits at 
#https://developer.twitter.com/en/docs/twitter-api/rate-limits

def get_sentiment(auth, tickers, date_since, include_retweets = False, num_tweets = 300):
  sentiment_signals = {}

  for ticker in tickers:
    
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    #Convert ticker into hashtag to help find more relevant results
    #For example, if looking to analyze sentiment on the S&P500, #SPY will likely return more relevant tweets 
    # -as opposed to "SPY" which could return unrelated tweets related to anything from politics or maybe the latest James Bond movie.
    tweets = tweepy.Cursor(api.search, q=("#" + ticker), lang='en', since=date_since, tweet_mode='extended').items(num_tweets)
    
    #Keep or filter out tweets that are retweets
    if include_retweets == True:
      tweets = [tweet.full_text for tweet in tweets]
    elif include_retweets == False:
      tweets = [tweet.full_text for tweet in tweets if tweet.full_text[0:2] != "RT"]
      
    analyzer = SentimentIntensityAnalyzer()
    
    #extracts the compound sentiment score for each tweet (taking into account negative, positive, and neutral sentiment)
    scores = [analyzer.polarity_scores(tweet)['compound'] for tweet in tweets] 
    
    #saves the average sentiment for all the tweets 
    sentiment_signals[ticker] = round(sum(scores)/len(scores), 4)

  return sentiment_signals

#Determine the time until the market opens 
def time_to_open(current_time):
    if current_time.weekday() <= 4:
        d = (current_time + timedelta(days=1)).date()
    else:
        days_to_mon = 0 - current_time.weekday() + 7
        d = (current_time + timedelta(days=days_to_mon)).date()
    next_day = datetime.datetime.combine(d, datetime.time(9, 30, tzinfo=tz))
    seconds = (next_day - current_time).total_seconds()
    return seconds

#While the number of tweets used to evaluate sentiment is set at 500 please take into account twitter API rate limits at: 
#https://developer.twitter.com/en/docs/twitter-api/rate-limits

def vader_sentiment_trader(twitter_auth, tickers, buy_threshold = 0.05, num_tweets = 250):
    print('vader_sentiment_trader started')
    while True:
        # Check if Monday-Friday
        if datetime.datetime.now(tz).weekday() >= 0 and datetime.datetime.now(tz).weekday() <= 4:
            # Checks market is open
            print('Trading day')
            if datetime.datetime.now(tz).time() > datetime.time(9, 30) and datetime.datetime.now(tz).time() <= datetime.time(15, 30):

                #Fetch the sentiment for each stock using  most recent tweets no more than 1 day old (default set to 500)
                signals = get_sentiment(twitter_auth, tickers, (datetime.datetime.today() - timedelta(days =1)).strftime("%Y-%m-%d"), include_retweets = False, num_tweets=num_tweets)
                for signal in signals:
                    
                    #If there is positive sentiment for the stock above the defined threshold (default set to 0.05), place a trade via the alpaca API
                    if signals[signal] > buy_threshold:
                        if signal not in [x.symbol for x in alpaca_api.list_positions()]:
                            logging.warning('{} {} - {}'.format(datetime.datetime.now(tz).strftime("%x %X"), signal, signals[signal]))
                            alpaca_api.submit_order(signal, 1, 'buy', 'market', 'day')
                            # print(datetime.datetime.now(tz).strftime("%x %X"), 'buying', signals[signal], signal)
                    else:
                        try:
                            alpaca_api.submit_order(signal, 1, 'sell', 'market', 'day')
                            logging.warning('{} {} - {}'.format(datetime.datetime.now(tz).strftime("%x %X"), signal, signals[signal]))
                        except Exception as e:
                            # print('No sell', signal, e)
                            pass
                            
                #Checks sentiment every 30 minutes (may be very interesting to experiment with further!)         
                time.sleep(1800)
            else:
                # Get time amount until open, sleep that amount
                print('Market closed ({})'.format(datetime.datetime.now(tz)))
                print('Sleeping', round(time_to_open(datetime.datetime.now(tz))/60/60, 2), 'hours')
                time.sleep(time_to_open(datetime.datetime.now(tz)))
        else:
            # If not trading day, find out how much until open, sleep that amount
            print('Market closed ({})'.format(datetime.datetime.now(tz)))
            print('Sleeping', round(time_to_open(datetime.datetime.now(tz))/60/60, 2), 'hours')
            time.sleep(time_to_open(datetime.datetime.now(tz)))

#Run strategy on S&P500 ETF
vader_sentiment_trader(twitter_auth, ['SPY'])