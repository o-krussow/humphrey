from datetime import datetime, timedelta
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import math


'''IDEAS        
        -Eventually will need to track how many trades each ticker has and how long we held each ticker so that we can incorporate management/holding and trading fees
'''

class Brokerage():
    def __init__(self, starting_cash = 10000, verbose = False):
        
        #Establishes the dictionary that keeps track of everything
        #Cash is in dollars, every security is in amount of stocks owned
        self.starting_cash = starting_cash
        self.cash = starting_cash
        self.portfolio = {'_cash': self.cash}
        self.verbose = verbose
        
        file = open('pickled_df', 'rb')
        self.price_df = pickle.load(file)
        file.close()

        self.price_df['Account_Total'] = self.starting_cash


    def buy(self, ticker, date, stock_quantity):
       
        date_price = self.price_df.at[date, ticker] 
        dollar_amount = stock_quantity * date_price

        #HANDLE THESE SOMEWHERE
        if round(dollar_amount, 2) > round(self.cash, 2):
            raise ValueError ("You do not have enough cash for this purchase")
        
        #Add a new ticker to holding if needed
        if ticker not in self.portfolio.keys():
            self.portfolio[ticker] = 0

        self.cash -= dollar_amount
        self.portfolio['_cash'] = self.cash
        self.portfolio[ticker] += stock_quantity

        if self.verbose == True:
            print(f"{date}:  Bought {stock_quantity} amount of {ticker} stock for ${dollar_amount}")
            print(f" Account Total: {self.holdings_total(date)} | Cash Total: {self.cash}\n")#might be too much


    def sell(self, ticker, date, stock_quantity):
        #this comes in as a negative number but it's easier for it not to be
        stock_quantity = stock_quantity * -1

        date_price = self.price_df.at[date, ticker]
        dollar_amount = stock_quantity * date_price

        #HANDLE THESE SOMEWHERE
        if ticker not in self.portfolio.keys():
            raise ValueError("Stock not even owned nerd")
        
        #Makes sure we aren't trying to sell more then we have
        if self.portfolio[ticker] < stock_quantity:
            raise ValueError("Trying to sell more than ya got goober")

        #updates our cash amount and resets our holding amount purchased, makes sure to not reset 
        self.cash += dollar_amount
        self.portfolio['_cash'] = self.cash
        self.portfolio[ticker] -= stock_quantity

        if self.verbose == True:
            print(f"{date}:  Sold {stock_quantity} amount of {ticker} stock for ${dollar_amount}")
            print(f" Account Total: {self.holdings_total(date)} | Cash Total: {self.cash}\n") #might be too much


    def holdings_total(self, date):
        total = 0
        for (ticker, stock_quantity) in self.portfolio.items():
            if ticker != '_cash':
                date_price = self.price_df.at[date, ticker] 
                total += stock_quantity * date_price

        return total

    def account_total(self, date):
        return self.holdings_total(date) + self.cash
    
    def log(self, date):
        self.price_df.loc[date, 'Account_Total'] = self.account_total(date)
    
    def get_percent_growth(self, end_date):
        final_holdings_total = self.holdings_total(end_date)
        percent_growth = (self.cash + final_holdings_total) / self.starting_cash - 1
        return percent_growth

    def better_than_IVV(self, start_date, end_date):
        IVV_start = self.price_df.at[start_date, "IVV"]
        IVV_end = self.price_df.at[end_date, "IVV"]
        IVV_growth = (IVV_end / IVV_start) - 1
        account_growth = self.get_percent_growth(end_date)
        return account_growth > IVV_growth

    def return_summary(self, start_date, end_date):
        final_holdings_total = self.holdings_total(end_date)

        output = "ACCOUNT SUMMARY".center(50, "=")

        output += "\nHoldings:\n"
        for (ticker, stock_quantity) in self.portfolio.items():
            if ticker != '_cash':
                date_price = self.price_df.at[end_date, ticker]
                cash_value = stock_quantity * date_price
                output += f"   {ticker}: {stock_quantity} owned, worth {cash_value}\n"

        output += "\nTotals:\n"
        output += f"Holdings Total: {final_holdings_total} | Cash Total: {self.cash} | Account Total: {self.cash + final_holdings_total}\n"

        output += "\nReturn:\n"
        output += f"Cash Growth: {self.cash + final_holdings_total - self.starting_cash} | Percent Return: {(self.cash+final_holdings_total) / self.starting_cash - 1} \n"

        output += "\nBenchmarks:\n"
        # AAPL_start = self.price_df.at[start_date, "AAPL"]
        # AAPL_end = self.price_df.at[end_date, "AAPL"]
        # output += f"Apple Dollar Growth: {AAPL_end - AAPL_start} | Apple Percent Growth: {(AAPL_end / AAPL_start) - 1} \n"

        IVV_start = self.price_df.at[start_date, "IVV"]
        IVV_end = self.price_df.at[end_date, "IVV"]
        output += f'IVV Start: {IVV_start} =====> IVV End: {IVV_end} \n'
        output += f"S&P Dollar Growth: {IVV_end - IVV_start} | S&P Percent Growth: {(IVV_end / IVV_start) - 1} \n"
        
        ACWX_start = self.price_df.at[start_date, "ACWX"]
        ACWX_end = self.price_df.at[end_date, "ACWX"]
        output += f'ACWX Start: {ACWX_start} =====> ACWX End: {ACWX_end} \n'
        output += f"exUS Dollar Growth: {ACWX_end - ACWX_start} | exUS Percent Growth: {(ACWX_end / ACWX_start) - 1}"

        return output


    def benchmarks(self, start_date, end_date):
        output = "Benchmarks".center(50, "=")

        IVV_start = self.price_df.at[start_date, "IVV"]
        IVV_end = self.price_df.at[end_date, "IVV"]
        output += f'\nIVV Start: {IVV_start} =====> IVV End: {IVV_end} \n'
        output += f"S&P Dollar Growth: {IVV_end - IVV_start} | S&P Percent Growth: {(IVV_end / IVV_start) - 1} \n"
        
        ACWX_start = self.price_df.at[start_date, "ACWX"]
        ACWX_end = self.price_df.at[end_date, "ACWX"]
        output += f'ACWX Start: {ACWX_start} =====> ACWX End: {ACWX_end} \n'
        output += f"exUS Dollar Growth: {ACWX_end - ACWX_start} | exUS Percent Growth: {(ACWX_end / ACWX_start) - 1}"

        return output


    def plot(self, tickers, start_date, end_date):
        df_plot = self.price_df.copy()
        df_plot = df_plot.iloc[df_plot.index.get_loc(start_date):]
        for ticker in tickers:
            df_plot[ticker] = df_plot[ticker]*math.floor(self.starting_cash/df_plot.at[start_date, ticker])
        tickers.append('Account_Total')
        df_plot[tickers].plot()
        plt.show()


    #potentially deprecated?
    def get_day_price_for_ticker(self, ticker, date):

        #check to see if date is applicable to ticker, if it isn't we recurse with an earlier day (so if we gave the date for a sunday, it will walk back to the last friday.)
        if date in self.prices_df.index():
            if self.price_df.at[date, ticker] == None:
                raise Exception("Price DNE yet")
            return self.price_df.at[date, ticker]
        else:
            #try subtracting a day, eventually we should get last closing price because date -> datestr will be in dates
            return self.get_day_price_for_ticker(ticker, date - timedelta(days=1)) 
        
    #Don't know if we'll use these, haven't gone through to make sure they work with pandas
    def get_prices(self, date, tdelta):
        #get_price_data_for_all_tickers wants date+tdelta to be after date, so this is a little wrapper so we can handle negative tdeltas
        #returns [date, date+tdelta] (inclusive)
        if date+tdelta > date:
            #then tdelta is positive
            return self.get_price_data_for_all_tickers(date, tdelta)
        else:
            #then tdelta is negative
            return self.get_price_data_for_all_tickers(date+tdelta, -1*tdelta)

    def get_price_data_for_all_tickers(self, date, tdelta):
        #self, datetime object, datetime delta

        #make inclusive of last date
        tdelta = tdelta + timedelta(days=1)

        price_range_dict = {}

        #Loop thru all the tickers (dict keys) in our csv dictionary
        for ticker in self.csvs:
            self.portfolio[ticker] = 0
            price_range_dict[ticker] = []
    
            #Set start date to initial date
            curr_date = date

            #Keep adding one day at a time until we reach date+tdelta, then we've collected prices for the whole range.
            while (curr_date != date + tdelta):
                curr_date_str = datetime.strftime(curr_date, "%Y-%m-%d")
                try:
                    #Get current price from get_day_price_for_ticker function since it will fill in gaps for us.
                    curr_price = self.get_day_price_for_ticker(ticker, curr_date)

                    #Appending date and price to our dictionary
                    price_range_dict[ticker].append((curr_date_str, curr_price))

                    #Increment day
                    curr_date = curr_date + timedelta(days=1)
                except Exception as e:
                    #If we run into exception, that means that prices didn't exist for this ticker at the beginning of the date range
                    #So we stop this while loop and move to the next ticker (next iteration of for loop)
                    #print(e)
                    break

        #This function WILL have keys for tickers that don't exist in the beginning of the date range, but WON'T have any prices/dates for them.
        return price_range_dict