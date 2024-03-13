
import datetime as dt
from strategy import Strategy
class Static_IVV(Strategy):
    def __init__(self, prices, start_cash = 10000):
        self.prices = prices
            #Dictionary {Ticker : [(Date, Price), (Date, Price), ... ]       }

        self.suggested_moves = {}

        self.US_prices = self.prices["IVV"]
        self.US_price_dict = {}
        for curr_date, curr_price in self.US_prices:
            self.US_price_dict[curr_date] = curr_price

        self.start_cash = start_cash
        self.first_purchase = True

    #60/40 
    def strategize(self, date, portfolio):
        
        date = dt.datetime.strftime(date, "%Y-%m-%d")

        if self.first_purchase == True:
           self.suggested_moves["IVV"] = (self.start_cash) / self.US_price_dict[date]  
           self.first_purchase = False
        else:
           self.suggested_moves["IVV"] = 0 

        return self.suggested_moves
