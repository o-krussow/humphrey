"""
Manager.py
Purpose: facilitate connection between brokerage and strategy for investment
Inputs: broker_acc (Brokerage object), date (datetime object of start date), 
        timedelta (negative integer representing data timespan)
Outputs: tbd
"""
import brokerage as br
import strategy as st
import datetime as dt

class Manager:
    def __init__(self, broker_acc, date = dt.datetime.now(), timedelta = -365):
        if timedelta >= 0:
            raise ValueError
        if date > dt.datetime.now():
            raise ValueError
        if type(broker_acc) != type(Brokerage(10000)):
            raise ValueError
        self.brokerage = broker_acc
        # create the investment changes variable
        self.investment_changes = {}
        # grab our portfolio and store it
        self.portfolio = self.brokerage.get_portfolio()
        # grab the current date
        self.date = date
        
        # create a strategy object for the current date
        self.strategy = st.Strategy(self.portfolio, self.brokerage.get_prices(self.date, timedelta))

    def update_investments(self, skip_confirmation = False):
        """Function to update your investments based on dated csv data using
        the strategy in strategy.py"""
        print("Updating investment strategy...")
        # update our investment changes
        self.investment_changes = self.strategy.strategize()
        # ask if they want to buy the new suggestions
        buy = self._confirm_updates(skip = skip_confirmation)
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
            if amount < 0:
                self.brokerage.buy(ticker, self.date, amount)
            else:
                self.brokerage.sell(ticker, self.date, amount)

    def __str__(self):
        output = ""
        output = self.brokerage.return_summary()
        return output

def backtesting():
    # create a brokerage account
    self.brokerage = br.Brokerage(10000)
    for i in range(0, 10):
        date = dt.datetime.now() + dt.timedelta(-365*i)
        manager = Manager(date = date) 
        manager.update_investments(skip_confirmation = True)
        print(manager)

if __name__ == "__main__":
    backtesting()

