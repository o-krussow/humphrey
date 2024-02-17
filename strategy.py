class Strategy():
    def __init__(self, prices, portfolio):
        self.prices = prices
            #Dictionary {Ticker : [(Date, Price), (Date+1, Price), ...]        }

        self.portfolio  = portfolio
        self.suggested_moves = {}

    def strategize(self):

        LOOK_BACK_PERIOD = 252

        SELL_THRESHOLD = 1.05

        BUY_THRESHOLD = 1.20
        STOCKS_BOUGHT_PER_DAY = 5
        CASH_PER_PURCHASE = 100


        percent_growth = {}

        #Creates a dictionary percent_growth {Ticker : Percent growth over lookback period}
        for (ticker, price_list) in self.prices.items():
           
            #checking if there is a year's worth of data behind each ticker
            if len(price_list) < LOOK_BACK_PERIOD:
                continue

            today = price_list[-1]
            look_back = price_list[-LOOK_BACK_PERIOD]

            percent_growth[ticker] =  (today[1] / look_back[1])


        #If the stock has gone up less than sell threshold, sell all of it
        for (ticker, amount) in self.portfolio.items():
            if percent_growth[ticker] < SELL_THRESHOLD:
                self.suggested_moves[ticker] = -amount


        #Sorts the growth tuples in descending order
        sorted_growth_tuples = sorted(percent_growth.items(), key=lambda tup: tup[1], reverse = True)

        for i in range(0, STOCKS_BOUGHT_PER_DAY):
            growth_tuple = sorted_growth_tuples[i]      #(ticker, price_growth)

            if growth_tuple[1] >= BUY_THRESHOLD:

                price_list = self.prices[growth_tuple[0]]
                today_price = price_list[-1][1]

                self.suggested_moves[growth_tuple[0]] = CASH_PER_PURCHASE / today_price

        

        return self.suggested_moves