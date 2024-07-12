

### Brokerage:
Maintains a dataframe of symbol prices, a portfolio, and a cash amount. Has functions Buy/Sell, as well as a variety of Summary functions.

### Backtest:
"Managing" file that sits between/above strategy and brokerage. Backtest iterates through the dates of the simulation period, feeding strategy the prices on a given day. Strategy returns a dictionary of Buy/Sell {tickers: quantities} which backtest then feeds to Brokerage to act on. Backtest takes a start and end date, as well as the strategy type and how verbose of a summary to print. If the strategy type requires any unique parameters, Backtest is initialized with a dictionary of these as well.

### Strategy:
Is initialized with any needed specific parameters via a dictionary. It also maintains a recollection of prices over the testing period. Each day that Strategize() is called (which should be every trading day), the Strategy class recieves a new day of price data which it then appends to its working historical knowledge. Strategize() returns a dictionary of Buy/Sell {tickers: quantities} based on the algorithim and given prices/inputs.


