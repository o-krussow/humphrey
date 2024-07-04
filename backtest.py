import brokerage as br
import new_test_strat as nts
import sys


def backtesting(strat, start_date, end_date, verbose = False):

    start_cash = 1000
    brokerage = br.Brokerage(start_cash)
    strategy = strat
    strategy = nts.new_test_strategy()


    all_dates = list(brokerage.price_df.index)
    start_date_index = all_dates.index(start_date)
    end_date_index = all_dates.index(end_date)

    for date in all_dates[start_date_index:end_date_index+1]:
        day_prices = brokerage.price_df.loc[date]
        investment_changes = strategy.strategize(day_prices, date, brokerage.portfolio)

        for ticker, amount in investment_changes.items():
            if amount < 0:
                brokerage.sell(ticker, date, amount)

        for ticker, amount in investment_changes.items():
            if amount > 0:
                brokerage.buy(ticker, date, amount)

    # Grab the percent return
    percent_return = brokerage.get_percent_growth(end_date)

    # Print it and relevant information
    if verbose == False:
        output = ""
        output += str(percent_return)+","
        for arg in sys.argv[1:]:
            output += arg + ","
        print(output)

    else:
        print(brokerage.return_summary(start_date, end_date))


if __name__ == "__main__":

    start_date = "1980-12-12"
    end_date = "2024-03-01"
    
    #           Strategy Name |        ^^^    | 
    # backtesting(sys.argv[1],    start_date,   end_date, True)
    
    backtesting("nts",    start_date,  end_date, True)