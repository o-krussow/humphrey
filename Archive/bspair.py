import datetime as dt
from Strategies.strategy import Strategy
class BSPair(Strategy):
    def __init__(self, prices, start_cash = 10000):
        self.prices = prices
            #Dictionary {Ticker : [(Date, Price), (Date, Price), ... ]       }

        self.suggested_moves = {}

        self.US_prices = self.prices["IVV"]
        self.US_price_dict = {}
        for curr_date, curr_price in self.US_prices:
            self.US_price_dict[curr_date] = curr_price

        self.exUS_prices = self.prices["ACWX"]
        self.exUS_price_dict = {}
        for curr_date, curr_price in self.exUS_prices:
            self.exUS_price_dict[curr_date] = curr_price
        
        self.bond_prices = self.prices["GOVT"]
        self.bond_price_dict = {}
        for curr_date, curr_price in self.bond_prices:
            self.bond_price_dict[curr_date] = curr_price


        self.look_back_period = dt.timedelta(days=-1)
        self.start_cash = start_cash

    def strategize(self, date, portfolio):
        
        #resetting moves each day
        self.suggested_moves["IVV"] = 0
        self.suggested_moves["ACWX"] = 0
        self.suggested_moves["GOVT"] = 0

        #This should take care of the first 30 days without a look back
        
        look_back_date_str = dt.datetime.strftime(date - self.look_back_period, "%Y-%m-%d")
        today_date_str = dt.datetime.strftime(date, "%Y-%m-%d")

        if (look_back_date_str) not in self.US_price_dict.keys():
            return self.suggested_moves

        dict_list = [self.US_price_dict, self.exUS_price_dict, self.bond_price_dict]
        ticker_list = ["IVV", "ACWX", "GOVT" ]


        percent_changes = []
        todays_prices = []

        for etf in dict_list:
            todays_price = etf[today_date_str]
            todays_prices.append(todays_price)
            lookback_price = etf[look_back_date_str]
            percent_changes.append((todays_price / lookback_price) - 1)

        #Percent_changes will have [US_change, exUS_change, bond_change]
        for pct_change in percent_changes:
            if pct_change > self.sell_threshold:
                pass #temp


        best_performer = 0 #temp
        best_performer_index = 0 #temp
        #if it already is held, maintain
        if portfolio[best_performer] > 0:
            return self.suggested_moves
        
        else:
            if self.first_purchase == True:
                cash_available = self.start_cash
                self.first_purchase = False

            else:
                cash_available = 0
                for ticker in ticker_list:
                    #if it wasn't the best performer, sell it all
                    if ticker != best_performer:
                        cash_available += portfolio[ticker] * todays_prices[ticker_list.index(ticker)]
                        self.suggested_moves[ticker] = - portfolio[ticker]

            self.suggested_moves[best_performer] = cash_available/todays_prices[best_performer_index]
            return self.suggested_moves


        
