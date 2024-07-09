from Strategies.strategy import Strategy
import math
import pandas as pd

class new_momentum(Strategy):
    def __init__(self, strategy_inputs):
        self.price_memory = pd.DataFrame()
        self.suggested_moves = {}
        self.lookback = strategy_inputs['lookback']
        self.tickers = strategy_inputs['tickers']

    
    def strategize(self, todays_prices, date, portfolio):
        row_df = pd.DataFrame([todays_prices], columns=todays_prices.index)
        row_df.index = [date]
        self.price_memory = pd.concat([self.price_memory, row_df])

        for ticker in self.tickers:
            self.suggested_moves[ticker] = 0

        if len(self.price_memory.index) < (self.lookback+1):
            return self.suggested_moves
        
        perc_change_df = self.price_memory.pct_change(self.lookback)
        perc_change_df = perc_change_df[self.tickers]           #limits to only look at given tickers
        best_performer = perc_change_df.loc[date].idxmax()

        cash_available = portfolio['_cash']
        for ticker in self.tickers:
            try:
                if ticker != best_performer:
                    cash_available += portfolio[ticker] * todays_prices[ticker]
                    self.suggested_moves[ticker] = - portfolio[ticker]
            except KeyError:
                continue

        self.suggested_moves[best_performer] += math.floor(cash_available/todays_prices[best_performer])
        return self.suggested_moves
