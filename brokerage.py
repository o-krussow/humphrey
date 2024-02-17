from os import listdir
from os.path import isfile, join
from datetime import datetime, timedelta

'''IDEAS
        -Make functions that show stuff like return or growth over time or something idk
        
        -Eventually will need to track how many trades each ticker has and how long we held each ticker so that we can incorporate management/holding and trading fees
'''

class Brokerage():
    def __init__(self, starting_cash = 10000):
        
        #Establishes the dictionary that keeps track of everything
        #Cash is in dollars, every security is in amount of stocks owned
        self.cash = starting_cash
        self._portfolio = {}
        self.csvs = {}

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
        print(f" Account Total: {self.account_total(date)} | Cash Total: {self.cash}")#might be too much


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
        print(f" Account Total: {self.account_total(date)} | Cash Total: {self.cash}") #might be too much



    def account_total(self, date):
        total = 0
        for (ticker, stock_quantity) in self._portfolio.items():
            date_price = 0 #HOWEVER WE ACCESS THE PRICE
            total += stock_quantity * date_price

        return total

    
    def return_summary(self, date):
        output = f" Account Total: {self.account_total(date)} | Cash Total: {self.cash}"
        for (ticker, stock_quantity) in self._portfolio.items():
            date_price = 0 #HOWEVER WE ACCESS THE PRICE
            cash_value = stock_quantity * date_price
            output + f"{ticker}: {stock_quantity} owned, worth {cash_value}\n"

        return output

    def _read_in_csvs(self):
        csvpath = "csvs/fixedcsv/"
        csvfilelist = [csvpath+f for f in listdir(csvpath) if isfile(join(csvpath, f))] 
        for csv in csvfilelist:
            with open(csv, "r") as f:
                file_contents = f.read()

            split_file = file_contents.split("\n")
            tmp_list = []
            for line in split_file:
                tmp_list.append(tuple(line.split(",")))
            
            self.csvs[csv.replace(csvpath, "").replace(".csv", "")] = tmp_list

    def get_day_price_for_ticker(self, ticker, date):
        datestr = date.strftime("%Y-%m-%d")
        dates = []

        for tup in self.csvs[ticker]:
            curr_date = tup[0]
            if len(tup) == 2 and curr_date != '':
                dates.append(tup[0]) #append the date string to list of dates
            else:
                dates.append("9999-99-99") # we don't want to skip because then the indexes wouldn't line up, so we insert a dummy date

        if datestr in dates:
            date_index = dates.index(datestr)
            return self.csvs[ticker][date_index][1]
        else:
            return self.get_day_price_for_ticker(ticker, date - timedelta(days=1)) #try subtracting a day, eventually we should get last closing price because date -> datestr will be in dates


if __name__ == "__main__":
    brok = Brokerage()

    brok._read_in_csvs()
    #print(brok.csvs["AAPL"])

    print(brok.get_day_price_for_ticker("AAPL", datetime.strptime("2024-02-14", "%Y-%m-%d")))


