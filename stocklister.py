#When you run this script it places the stocks in a list that you would be able to import to a 
#main script so it runs all the stocks that are in a cvs file as a screener
#
#
#
BARS_URL = "https://data.alpaca.markets/v1/bars"
from csv import writer
import config


holdings = open('data/ccc.csv').readlines()

symbols = [holding.split(',')[0].strip() for holding in holdings][1:185]  # the [0] represents the column you want to pull, and the [1:] at the end represents removing the stocks at the 1 postiiton 
#symbols = ",".join(symbols)                                              # ALPACA WANTS THE STOCKS LIKE AA,BA NOT 'AA','BA' REMOVES THE COMA AND PUTS IN A LIST

print(symbols)
