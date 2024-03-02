"""
Manager.py
Purpose: facilitate connection between brokerage and strategy for investment
Inputs: broker_acc (Brokerage object), date (datetime object of start date), 
        timedelta (integer representing data timespan)
Outputs: tbd
"""
import brokerage as br
import ss_bsp_strategy as bsp
import datetime as dt
import sys
import pickle

class Manager:
    def __init__(self, strat, start_cash = 10000, date = dt.datetime.now(), timedelta = dt.timedelta(days=2*365)):
        #if timedelta >= 0: ?
        #    raise ValueError
        if date > dt.datetime.now():
            raise ValueError("Invalid date")

        #loading pickled data
        file = open('pickled_csvs', 'rb')
        self.csvs = pickle.load(file)
        file.close()

        # create the investment changes variable
        self.investment_changes = {}

        # initialize the brokerage account
        self.brokerage = br.Brokerage(self.csvs, start_cash)

        # grab our portfolio and store it
        self.portfolio = self.brokerage.get_portfolio()

        # grab the current date
        self.date = date
       
        self.tdelta = timedelta
        

        
        if strat == "ss_bsp":
            # create a bsp strategy object for the current date                                                    buy threshold&sell threshold in tuple
            self.strategy = bsp.SS_BSP_Strategy(self.portfolio, self.brokerage.get_prices(self.date, self.tdelta), sys.argv)
        #elif strat == "example":
        #   self.strategy = example.Example_Strategy(self.portfolio, self.bro...
        else:
            raise ValueError(f"{strat} is not a valid strategy")

    def update_investments(self, skip_confirmation = False):
        """Function to update your investments based on dated csv data using
        the strategy in strategy.py"""
        # update our investment changes
        self.investment_changes = self.strategy.strategize(self.date)
        # ask if they want to buy the new suggestions
        
        #buy = self._confirm_updates(skip = skip_confirmation)
        buy = True
        if buy:
            self._buy_updates()

    def _confirm_updates(self, skip = False):
        """Function to confirm whether the user wants to go through with the
        investments"""
        print(f"Investment changes from strategy:\n {self.investment_changes}")
        if not skip:
            # grab user input on stock change confirmation
            ui = input("Confirm these changes? (y/n): ").lower()
            while (ui != "y" and ui != "n"):
                print("Please enter a valid input")
                ui = input("Confirm these changes? (y/n): ").lower()

            # if they didn't want to change it, return false
            if ui == "n":
                print("Okay! Figure it out!")
                return False

        # if they did want to change it or the program is set to skip this step
        # return true
        else:
            print("Set to skip confirmation...")
        print("Proceeding to purchase portfolio updates...") 
        return True
    def _buy_updates(self):
        """Do the investing"""
        for ticker, amount in self.investment_changes.items():
            if amount > 0:
                self.brokerage.buy(ticker, self.date, amount)
            elif amount < 0:
                self.brokerage.sell(ticker, self.date, amount)
            else:
                #amount == 0
                continue

    def __str__(self):
        output = ""
        output = self.brokerage.return_summary(self.date, self.date + self.tdelta)
        return output

def backtesting(strat, verbose = False):

    #Start date
    date = dt.datetime.strptime("2020-01-01", "%Y-%m-%d")
  
    timedelta = dt.timedelta(days=2*365)

    # Make the manager
    start_cash = 10000
    manager = Manager(strat, start_cash, date = date, timedelta = timedelta) 

    #Going for 365*2 days after start date
    for i in range(2*365):
        date = date + dt.timedelta(days=1)
        manager.date = date
        manager.update_investments(skip_confirmation = True)

    # Grab the percent return
    percent_return = manager.brokerage.get_percent_growth(date + timedelta)

    # Print it and relevant information
    output = ""
    output += str(percent_return)
    for arg in sys.argv[1:]:
        output += arg + ","
    print(output)

if __name__ == "__main__":
    backtesting(sys.argv[1], True)

