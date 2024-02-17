

### Brokerage:
Is a stand-in for the API we'll use in real life once backtesting is done

### Manager:
"Top level" file that sits between/above strategy and brokerage. When a strategy wants to buy a stock, it goes through manager, then goes to brokerage. When a strategy wants to check stock prices, it goes through the manager, which then communicates with brokerage. The thinking is that manager should print a summary of all the trades in csv format, that way it's easy to open the output file in excel or whatever to appease chase.

### Strategy:
This is what we'll be testing in backtesting, trying to find the strategy to maximize profits.


