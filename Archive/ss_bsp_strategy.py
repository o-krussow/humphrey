import datetime as dt
from Strategies.strategy import Strategy

class SS_BSP_Strategy(Strategy):
    def __init__(self, prices, cmdline_args):
        self.prices = prices
            #Dictionary {Ticker : [(Date, Price), (Date, Price), ...]        }

        self.buy_threshold, self.sell_threshold = float(cmdline_args[2]), float(cmdline_args[3])

        self.suggested_moves = {}

        self.apple_price = prices["AAPL"]

        self.apple_price_dict = {}
        for curr_date, curr_price in self.apple_price:
            self.apple_price_dict[curr_date] = curr_price

        self.holding_stock = False
        self.sell_price = 0

    
    def strategize(self, date, portfolio):
        
        #Asks itself, "Should I buy Apple on this date?"

        todays_price = self.apple_price_dict[dt.datetime.strftime(date, "%Y-%m-%d")]
        try:
            yesterdays_price = self.apple_price_dict[dt.datetime.strftime(date - dt.timedelta(days = 1), "%Y-%m-%d")]
        except KeyError:
            self.suggested_moves["AAPL"] = 0
            return self.suggested_moves

        self.suggested_moves["AAPL"] = 0

        pctchange = (todays_price / yesterdays_price) - 1

        if self.holding_stock == False:
            #if percentage change is lower than buy percentage but not *100 (eg -0.02)
            if pctchange <= self.buy_threshold:
                self.suggested_moves["AAPL"] = 1
                self.holding_stock = True
                self.sell_price = (todays_price * (1 + self.sell_threshold))

        if self.holding_stock == True:
            if todays_price >= self.sell_price:
                self.suggested_moves["AAPL"] = -1
                self.holding_stock = False

        return self.suggested_moves



