
import alpaca_trade_api as tradeapi
import time
import datetime
from datetime import timedelta
from pytz import timezone
import btalib
tz = timezone('EST')

api = tradeapi.REST('PK5IZVQ89X3BUBWSP1JC',
                    'dyYUFtBdNicjfL8oRg9ht4mYoyI3IbLptus3qgH0',
                    'https://paper-api.alpaca.markets')

import logging
logging.basicConfig(filename='./new_5min_ema.log', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('{} logging started'.format(datetime.datetime.now().strftime("%x %X")))

def get_data_bars(symbols, rate, slow, fast):
    data = api.get_barset(symbols, rate, limit=500).df
    for x in symbols:
        data.loc[:, (x, 'fast_ema')] = data[x]['close'].rolling(window=fast).mean()
        data.loc[:, (x, 'slow_ema')] = data[x]['close'].rolling(window=slow).mean()
    return data

def get_signal_bars(symbol_list, rate, ema_slow, ema_fast):
    data = get_data_bars(symbol_list, rate, ema_slow, ema_fast)
    signals = {}
    for x in symbol_list:
        if data[x].iloc[-1]['fast_ema'] > data[x].iloc[-1]['slow_ema']: signal = 1
        else: signal = 0
        signals[x] = signal
    return signals

def time_to_open(current_time):
    if current_time.weekday() <= 4:
        d = (current_time + timedelta(days=1)).date()
    else:
        days_to_mon = 0 - current_time.weekday() + 7
        d = (current_time + timedelta(days=days_to_mon)).date()
    next_day = datetime.datetime.combine(d, datetime.time(9, 30, tzinfo=tz))
    seconds = (next_day - current_time).total_seconds()
    return seconds

def run_checker(stocklist):
    print('run_checker started')
    while True:
        # Check if Monday-Friday
        if datetime.datetime.now(tz).weekday() >= 0 and datetime.datetime.now(tz).weekday() <= 4:
            # Checks market is open
            print('Trading day')
            if datetime.datetime.now(tz).time() > datetime.time(9, 30) and datetime.datetime.now(tz).time() <= datetime.time(15, 30):
                signals = get_signal_bars(stocklist, '5Min', 200, 50)
                for signal in signals:
                    if signals[signal] == 1:
                        if signal not in [x.symbol for x in api.list_positions()]:
                            logging.warning('{} {} - {}'.format(datetime.datetime.now(tz).strftime("%x %X"), signal, signals[signal]))
                            api.submit_order(signal, 1, 'buy', 'market', 'day')
                            print(datetime.datetime.now(tz).strftime("%x %X"), 'buying', signals[signal], signal)
                    else:
                        try:
                            while True:
                                
                                api.submit_order(signal, 1, 'sell', 'market', 'day')
                                logging.warning('{} {} - {}'.format(datetime.datetime.now(tz).strftime("%x %X"), signal, signals[signal]))
                        except Exception as e:
                            # print('No sell', signal, e)
                            pass

                time.sleep(60)
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


holdings = open('data/ccc.csv').readlines()        ##================================This is a pulled list from IBD stock screener
symbols = [holding.split(',')[0].strip() for holding in holdings][1:185]  # the [0] represents the column you want to pull, and the [1:] at the end represents removing the stocks at the 1 postiiton in the file
symbols = ",".join(symbols)                         #####    ================+++++=++++ THis makes the symbols in a pattern of  'BA','AA' etc....

stocks = ['AVLR', 'BOOT', 'EDUC', 'GNSS', 'HBP', 'MOD', 'PCTY', 'SMTS', 'SNAP', 'SOL', 'TCON', 'TKR', 'TRIB', 'TVTX', 'BWEN', 'BXC', 'CALX', 'CSWI', 'HDS', 'IDN', 'IIPR', 'LASR', 'MTCH', 'STNE', 'STRT', 'TBK', 'WCC', 'WMS', 'ACMR', 'ACU', 'BSTC', 'DKS', 'FENG', 'GFL', 'IESC', 'LAZY', 'LMB', 'LMPX', 'NIU', 'PWR', 'SAIA', 'SAIL', 'STRO', 'VRTS', 'AMRK', 'CAI', 'CAMT', 'COHU', 'CORT', 'CRNC', 'EV', 'FCEL', 'FUV', 'GSL', 'GTLS', 'HASI', 'IRCP', 'LWAY', 'PDEX', 'QRTEA', 'RYI', 'SI', 'TGH', 'TRQ', 'BIG', 'BLD', 'CDNA', 'CELH', 'CTLT', 'ENPH', 'FIZZ', 'HALO', 'JHX', 'JKS', 'KNSL', 'LCUT', 'LE', 'NLS', 'NVCR', 'PINS', 'REGI', 'SSTK', 'SWBI', 'TIGR', 'ZDGE', 'CLCT', 'DOCU', 'EXPI', 'GDOT', 'IEA', 'LI', 'LITB', 'LL', 'LSCC', 'MRVL', 'MYRG', 'NIO', 'RVP', 'SNBR', 'SPSC', 'STAA', 'TCS', 'UMC', 'WTRE', 'ZEN', 'AAXN', 'BEKE', 'BLDR', 'CMBM', 'DAR', 'DOYU', 'FIVN', 'FORM', 'FVRR', 'GRVY', 'JOE', 'MATX', 'OIIM', 'PDD', 'PNTG', 'PTON', 'SGC', 'TSM', 'TTGT', 'TUP', 'VRT', 'VSTO', 'AMRC', 'BL', 'BRP', 'CLGX', 'COOP', 'ELA', 'GNRC', 'HEAR', 'HIBB', 'HIMX', 'HZNP', 'HZO', 'IIVI', 'JYNT', 'LOB', 'MAX', 'PRSC', 'PW', 'QCOM', 'QDEL', 'RBBN', 'SQ', 'WD', 'AMD', 'AOSL', 'APPS', 'APT', 'AVNW', 'BGFV', 'BMCH', 'BRKS', 'COWN', 'CROX', 'CRSR', 'DQ', 'ENTG', 'ESCA', 'ETSY', 'FCX', 'FLGT', 'FSLR', 'FUTU', 'GRBK', 'GRWG', 'IPHI', 'JD', 'LOGI', 'MBIN', 'MED', 'PFSI', 'RGEN', 'RNDB', 'TER', 'VIPS', 'XPEL', 'YALA', 'YETI']                                #-----------------------============ This is for putting all the screened stocks into the loop 

run_checker(stocks)