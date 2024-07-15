from backtest import backtesting
import pandas as pd
from util.calculate_year_dif import calculate_year_dif
from util.generate_combos import generate_combos

def multi_date_range_test(strat: tuple, strategy_inputs: dict, test_span = 'years') -> pd.DataFrame: 
    combinations = generate_combos(test_span, strategy_inputs['tickers'])

    lod = [] #list of dictionaries
    for start_date, end_date in combinations:
        d = {'start_date': start_date, 'end_date': end_date, 'total_years': calculate_year_dif(start_date, end_date)}
        returned_dict = backtesting(strat, start_date, end_date, strategy_inputs, 'panda')
        d.update(returned_dict)
        lod.append(d)
    
    results_df = pd.DataFrame(lod)
    results_df['annual_return'] = results_df['percent_growth'] / results_df['total_years']
    avg_annual_return = results_df['annual_return'].mean()
    outperfrom_ratio = results_df['better_than_IVV'].mean()
    best_performance = results_df.loc[results_df['annual_return'].idxmax(), ['start_date', 'end_date', 'percent_growth', 'annual_return']].tolist()
    worst_performance = results_df.loc[results_df['annual_return'].idxmin(), ['start_date', 'end_date', 'annual_return']].tolist()
    avg_recent_return = results_df['annual_return'].tail(10).mean()
    recent_outperformance = results_df['better_than_IVV'].tail(10).mean()

    #will eventually return all these metrics once slurm is going
    print(f'Average Annual Return: {avg_annual_return}')
    print(f'Percent Outperformed S&P500: {outperfrom_ratio}')
    print(f'Best Performance: {best_performance}')
    print(f'Worst Performance: {worst_performance}')
    print(f'Recent Average Annual Return: {avg_recent_return}')
    print(f'Recent Outperfromance Ratio: {recent_outperformance}')



# strat = ('.long_TQQQ', 'Long_TQQQ')
# strategy_inputs = {'tickers': 'TQQQ'}

strat = ('.new_momentum', 'New_Momentum')
strategy_inputs = {'lookback' : 50, 'tickers': ['IVV', 'ACWX', 'GOVT']}
multi_date_range_test(strat, strategy_inputs, test_span='months')