from strategy import Strategy
import random
import pandas as pd

class new_test_strategy(Strategy):
    def __init__(self):
        self.price_memory = pd.DataFrame()
        self.suggested_moves = {}
        self.holding_stock = False
        self.sell_price = 0

    
    def strategize(self, todays_prices, date, portfolio):
        row_df = pd.DataFrame([todays_prices], columns=todays_prices.index)
        row_df.index = [date]
        self.price_memory = pd.concat([self.price_memory, row_df])

        self.suggested_moves["AAPL"] = 0
        if self.holding_stock == False:
            if random.choice([0, 1]) == 1:
                self.suggested_moves["AAPL"] = 1
                self.holding_stock = True

        elif self.holding_stock == True:
            if random.choice([0, 1]) == 1:
                self.suggested_moves["AAPL"] = -1
                self.holding_stock = False

        return self.suggested_movesfrom 