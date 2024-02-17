'''IDEAS
        -Make verbose option that prints out whenever a purchase is made, or better yet, prints to a file
        -Make functions that show stuff like return or growth over time or something idk
        
        -Eventually will need to track how many trades each ticker has and how long we held each ticker so that we can incorporate management/holding and trading fees
'''

class Brokerage():
    def __init__(self, starting_cash = 10000):
        
        #Establishes the dictionary that keeps track of everything
        #Cash is in dollars, every security is in amount of stocks owned
        self.cash = starting_cash
        self._portfolio = {}

    def get_portfolio(self):
        return self._portfolio

    def buy(self, ticker, date, stock_quantity):
       
        date_price = 0 #HOWEVER WE ACCESS THE PRICE
        dollar_amount = stock_quantity * date_price

        #HANDLE THESE SOMEWHERE
        if dollar_amount > self.cash:
            raise ValueError ("You do not have enough cash for this purchase")
        
        #Add a new ticker to holding if needed
        if ticker not in self._portfolio.keys():
            self._portfolio[ticker] = 0

        self.cash -= dollar_amount
        self._portfolio[ticker] += stock_quantity

        print(f"{date}:  Bought {stock_quantity} amount of {ticker} stock for ${dollar_amount}")


    def sell(self, ticker, date, stock_quantity):
       
        date_price = 0 #HOWEVER WE ACCESS THE PRICE
        dollar_amount = stock_quantity * date_price

        #HANDLE THESE SOMEWHERE
        if ticker not in self._portfolio.keys():
            raise ValueError("Stock not even owned nerd")
        
        #Makes sure we aren't trying to sell more then we have
        if self._portfolio[ticker] < stock_quantity:
            raise ValueError("Trying to sell more than ya got goober")

        #updates our cash amount and resets our holding amount purchased, makes sure to not reset 
        self.cash += dollar_amount
        self._portfolio[ticker] -= stock_quantity

        print(f"{date}:  Sold {stock_quantity} amount of {ticker} stock for ${dollar_amount}")



    def account_total(self, date):
        total = 0
        for (ticker, stock_quantity) in self._portfolio.items():
            date_price = 0 #HOWEVER WE ACCESS THE PRICE
            total += stock_quantity * date_price

    
    def __str__(self):
        output = ""
        for (ticker, stock_quantity) in self._portfolio.items():
            date_price = 0 #HOWEVER WE ACCESS THE PRICE
            cash_value = stock_quantity * date_price
            output + f"{ticker}: {stock_quantity} owned, worth {cash_value}\n"

    
