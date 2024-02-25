"""
Manager.py
Purpose: facilitate connection between brokerage and strategy for investment
Inputs: broker_acc (Brokerage object), date (datetime object of start date), 
        timedelta (negative integer representing data timespan)
Outputs: tbd
"""
import brokerage as br
import ss_bsp_strategy as st
import datetime as dt
import sys

class Manager:
    def __init__(self, broker_acc, date = dt.datetime.now(), timedelta = dt.timedelta(days=2*365)):
        #if timedelta >= 0: ?
        #    raise ValueError
        if date > dt.datetime.now():
            raise ValueError
        if type(broker_acc) != type(br.Brokerage(10000)):
            raise ValueError
        self.brokerage = broker_acc
        # create the investment changes variable
        self.investment_changes = {}
        # grab our portfolio and store it
        self.portfolio = self.brokerage.get_portfolio()
        # grab the current date
        self.date = date
       
        self.tdelta = timedelta

        # create a strategy object for the current date                                              buy threshold          sell threshold
        self.strategy = st.Strategy(self.portfolio, self.brokerage.get_prices(self.date, self.tdelta), float(sys.argv[1]), float(sys.argv[2]))

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
        output = self.brokerage.return_summary(self.date + self.tdelta)
        return output

#def backtesting():
#    # create a brokerage account
#    brokerage = br.Brokerage(10000)
#    #0 thru -10 years
#    for i in range(1, 10):
#        date = dt.datetime.strptime("2024-01-02", "%Y-%m-%d") - dt.timedelta(days=365*i)
#        #for every year, we make another manager/test of strategy?
#        manager = Manager(brokerage, date = date) 
#        for day in range(0, 365):
#            print(manager.date)
#            manager.date = manager.date + dt.timedelta(days = 1)
#            manager.update_investments(skip_confirmation = True)
#        print(manager)


def backtesting():
    #Just wanted to simplify this for now
    brokerage = br.Brokerage(10000)

    #Start date
    date = dt.datetime.strptime("2020-01-01", "%Y-%m-%d")
  
    timedelta = dt.timedelta(days=2*365)

    manager = Manager(brokerage, date = date) 

    #Going for 365*2 days after start date
    for i in range(2*365):
        date = date + dt.timedelta(days=1)
        manager.date = date
        manager.update_investments(skip_confirmation = True)
    print(manager)


if __name__ == "__main__":
    backtesting()






