from strategy import Strategy
import random

class new_test_strategy(Strategy):
    def __init__(self):
        self.suggested_moves = {}
        self.holding_stock = False
        self.sell_price = 0

    
    def strategize(self, todays_prices, portfolio):
        if self.holding_stock == False:
            #if percentage change is lower than buy percentage but not *100 (eg -0.02)
            if random.choice([0, 1]) == 1:
                self.suggested_moves["AAPL"] = 1
                self.holding_stock = True

        if self.holding_stock == True:
            if random.choice([0, 1]) == 1:
                self.suggested_moves["AAPL"] = -1
                self.holding_stock = False

        return self.suggested_moves



