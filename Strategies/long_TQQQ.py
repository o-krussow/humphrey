from Strategies.strategy import Strategy
import pandas as pd
import math

strategy_inputs = {'tickers': 'TQQQ'}
class Long_TQQQ(Strategy):
    def __init__(self, strategy_inputs):
        self.price_memory = pd.DataFrame()
        self.suggested_moves = {}
        self.first_purchase = True

    
    def strategize(self, todays_prices, date, portfolio):
        cash_available = portfolio['_cash']
        self.suggested_moves['TQQQ'] = math.floor(cash_available/todays_prices['TQQQ'])
        self.first_purchase 
        return self.suggested_moves