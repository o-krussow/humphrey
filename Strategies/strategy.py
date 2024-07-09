"""
Contains the Strategy interface, which is used to implement different strategies for the trading bot.
The strategize method is called by the backtesting function in backtest.py, and should return a dictionary
of tickers and how much to buy/sell from them.

Should consider how necessary this is - it's nice to have in case we want to add more but as with
most interfaces it kinda just sits around and does nothing
"""
class Strategy():
    def strategize(self):
        """Takes argv inputs and uses them to strategize.
        Should return a *?dictionary?* of tickers and how much to buy/sell from them.
        Inputs vary depending on strategy implementation."""
        pass

    # can add more if we need to

