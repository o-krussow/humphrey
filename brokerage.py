'''IDEAS
        -Make verbose option that prints out whenever a purchase is made, or better yet, prints to a file
        -Make functions that show stuff like return or growth over time or something idk
        -Make __str__ that prints the holdings dictionary pretty
        
        -Eventually will need to track how many trades each ticker has and how long we held each ticker so that we can incorporate management/holding and trading fees
'''

class Brokerage():
    def __init__(self, starting_cash = 10000):
        
        #Establishes the dictionary that keeps track of everything
        #Cash is in dollars, every security is in amount of stocks owned
        self.cash = starting_cash
        self.holdings = {}


    def buy(self, ticker, ticker_dataframe, date, dollar_amount = 0):
        #HANDLE THESE SOMEWHERE
        #Makes sure we have enough cash to buy
        if dollar_amount > self.cash:
            raise ValueError
        
        #Makes sure date is valid
        if date not in ticker_dataframe['Date'].tolist():
            raise ValueError    #should we raise a different error to distinguish between the two?
        
        #Makes sure we only chose one purchase method
        if dollar_amount > 0 and percentage > 0:
            raise ValueError
        
        #This allows us below to keep adding on investments into the same thing, otherwise, we would need to reset everytime at 0.
        try:
            self.holdings[ticker]
        except:
            self.holdings[ticker] = 0
        
        #Finds the price at said date and total cash_used
        date_price = self.price_from_date(date, ticker_dataframe)
        cash_used = self.cash * percentage + dollar_amount  #since one must be zero, this should work for both cases
        
        #calculates how much we are purchasing
        amount_purchased = cash_used / date_price

        #resets our cash amount and sets our new holding amount purchased, makes sure to not reset 
        self.cash = self.cash - cash_used
        self.holdings[ticker] = self.holdings[ticker] + amount_purchased



    def sell(self, ticker, ticker_dataframe, date, dollar_amount = 0, percentage = 0):
        #HANDLE THESE SOMEWHERE
        #Makes sure we even hold the stock
        try:
            self.holdings[ticker]
        except:
             ValueError
        
        #Makes sure date is valid
        if date not in ticker_dataframe['Date'].tolist():
            raise ValueError    #should we raise a different error to distinguish between the two?
        
        #Makes sure we only chose one sell method
        if dollar_amount > 0 and percentage > 0:
            raise ValueError
        
        #Finds the price at said date
        date_price = self.price_from_date(date, ticker_dataframe)
    
        #finds how many stocks we're selling
        stock_amount_selling = self.holdings[ticker] * percentage + dollar_amount/date_price  #since one must be zero, this should work for both cases
        cash_selling = stock_amount_selling * date_price

        #Makes sure we aren't trying to sell more then we have
        if self.holdings[ticker] < stock_amount_selling:
            raise ValueError

        #updates our cash amount and resets our holding amount purchased, makes sure to not reset 
        self.cash = self.cash + cash_selling
        self.holdings[ticker] = self.holdings[ticker] - stock_amount_selling



    def price_from_date(self, date, dataframe):
        i = dataframe.index[dataframe["Date"] == date].tolist()
        return dataframe[i]["Close"]