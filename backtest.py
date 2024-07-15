import brokerage as br
import importlib

def backtesting(strat: tuple, start_date: str, end_date: str, strategy_inputs: dict, output: str):
    '''
    Parameters:
    strat: (file_name, class_name)
    start_date: 'yyyy-mm-dd'
    end_date: 'yyyy-mm-dd'
    strategy_inputs: {} -> strategy dependent
    output: "plot" or "panda"

    Returns:
    plot -> extensive summary (Brokerage.return_summary)
            plot of account growth 

    panda -> {'final portfolio': dict, 'percent_growth': float, 'better_than_IVV': bool}

    '''
    start_cash = 1000
    brokerage = br.Brokerage(start_cash)
    strat_file = importlib.import_module(strat[0], package='Strategies')
    strat_class = getattr(strat_file, strat[1])
    strategy = strat_class(strategy_inputs)

    df = brokerage.price_df[strategy_inputs['tickers']].dropna()
    all_dates = list(df.index)
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
    if output == 'panda':
        return_dict = {'final portfolio': brokerage.portfolio, 
                       'percent_growth': brokerage.get_percent_growth(end_date), 
                       'better_than_IVV': brokerage.better_than_IVV(start_date, end_date)}
        return return_dict

    elif output == 'plot':
        print(brokerage.return_summary(start_date, end_date))
        brokerage.plot(strategy_inputs['tickers'], start_date, end_date)
    
    else:
        raise TypeError("Output received unexpected input... you fool")
