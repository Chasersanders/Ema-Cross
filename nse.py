#####NSE stock
import robin_stocks as rh
#install these libraries - nsetools,pprint,csv
from nsetools import Nse
from pprint import pprint
from csv import writer
rh.login("stephanielc8@gmail.com", "Love8899!!")

#function to insert things into csv
def append_list_as_row(file_name, list_of_elem):
# Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
# Create a writer object from csv module
        csv_writer = writer(write_obj)
# Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

nse= Nse()

#this list just stores names of the required stocks so that
#you can use this directly into your code and use accordingly
stocks_list = []

#top gainers
top_gainers = rh.markets.get_top_movers_sp500('up', info='symbol')

#remove comment of the next line to see all fields available
#pprint(top_gainers[0])

#insert column titles
row=['Stock name','Open price','High price','Low price','Previous price','Volume','Ltp']

#inserts the columns names into the csv file
append_list_as_row('topGainers.csv',row)


#change value of range to receive your required numbers of stocks max-10
for i in range(10):
    stock_name=top_gainers[i]['symbol']


    row=[stock_name]

    #file is named topGainers
    append_list_as_row('topGainers.csv',row)

    #adds the names of gainer stocks to the list
    stocks_list.append(stock_name)



#top losers
top_losers = nse.get_top_losers()

#remove comment of the next line to see all fields available
#pprint(top_losers[0])

#insert column titles
row=['Stock name','Open price','High price','Low price','Previous price','Volume','Ltp']

#inserts the columns names into the csv file
append_list_as_row('topLosers.csv',row)

#change value of range to receive your required numbers of stocks max-10
for i in range(10):
    stock_name=top_losers[i]['symbol']
    open_price=top_losers[i]['openPrice']
    previous_price=top_losers[i]['previousPrice']
    volume=top_losers[i]['tradedQuantity']
    high_price=top_losers[i]['highPrice']
    low_price=top_losers[i]['lowPrice']
    ltp=top_losers[i]['ltp']
    row=[stock_name,open_price,high_price,low_price,previous_price,volume,ltp]

    #file is named topLosers.csv
    append_list_as_row('topLosers.csv',row)

    #adds the name of the loser stocks
    stocks_list.append(stock_name)

#remove the next line's comment to see the stock names or use the list in your code directly
#print(stocks_list)