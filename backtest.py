import brokerage as br
import Strategies.new_momentum as nm # might find programatic way to import these


def backtesting(strat, start_date, end_date, strategy_inputs, verbose = 0):

    start_cash = 1000
    brokerage = br.Brokerage(start_cash)
    strategy = strat
    # TODO: should programatically determine which strategy to use
    strategy = nm.new_momentum(strategy_inputs)


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
        
        brokerage.log(date)

    # Grab the percent return
    percent_return = brokerage.get_percent_growth(end_date)
    account_total = brokerage.account_total(end_date)

    # 3 different levels of printing results
    if verbose == 0:
        if brokerage.better_than_IVV(start_date, end_date):
            output = f'Account Total: {account_total}, Percent Return: {percent_return}, '
            for key, value in strategy_inputs.items():
                output += f'{key}: {value} '
            print(output)
    
    elif verbose == 1:
        output = f'Account Total: {account_total}, Percent Return: {percent_return}, '
        for key, value in strategy_inputs.items():
            output += f'{key}: {value} '
        print(output)

    elif verbose == 2:
        print(brokerage.return_summary(start_date, end_date))
        brokerage.plot(strategy_inputs['tickers'], start_date, end_date)


if __name__ == "__main__":
### Mulit-Date range and strategy parameter tests
    start_dates = ["2012-02-24", "2013-02-25", "2014-02-24", "2015-02-24", "2016-02-24", 
                   "2017-02-24", "2018-02-23", "2019-02-25", "2020-02-24", "2021-02-24"]
    end_dates = ["2015-02-24", "2016-02-24", "2017-02-24", "2018-02-23", "2019-02-25", 
                "2020-02-24", "2021-02-24", "2022-02-24", "2023-02-24", "2024-02-23"]
    combinations = [(start, end) for start in start_dates for end in end_dates if start < end]

    benchmarks = br.Brokerage()

    # for start_date, end_date in combinations:
    #     print(f'\n\n{start_date} through {end_date}\n')
    #     print(benchmarks.benchmarks(start_date, end_date))
    #     print('\nStrategies:\n')
    #     for lookback in range(30, 150, 10):
    #         strategy_inputs = {'lookback' : lookback, 'tickers': ['IVV', 'ACWX', 'GOVT']}
    #         backtesting("new_momentum", start_date,  end_date, strategy_inputs, 0)


###In-Depth look at a specific scenario
    start_date = "2012-02-24"
    end_date = "2024-03-01"
    strategy_inputs = {'lookback' : 50, 'tickers': ['IVV', 'ACWX', 'GOVT']}
    backtesting("new_momentum", start_date,  end_date, strategy_inputs, 2)