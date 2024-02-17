"""
Manager.py
Purpose: facilitate connection between brokerage and strategy for investment
Inputs: tbd
Outputs: tbd
"""
import brokerage as br
import strategy as st

class Manager:
    def __init__(self):
        self.brokerage = br.Brokerage(x, x, x)
        self.investment_changes = []
        self.portfolio = self.brokerage.get_portfolio() #placeholder function

    def update_investments(self):
        self.investment_changes = []
        self.investment_changes = st.strategize(self.portfolio) #placeholder function
        return 
 
    def __str__(self):
        output = ""
        output = str(self.brokerage)
        return output

def main():
    manager = Manager()
    print(manager)
    

if __name__ == "__main__":
    main()

