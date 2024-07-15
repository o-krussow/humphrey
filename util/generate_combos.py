from datetime import datetime
from dateutil.relativedelta import relativedelta
import pickle
import pandas as pd
from itertools import combinations


def generate_combos(time_span, tickers):
    file = open('Data/Pickles/pickled_df', 'rb')
    df = pickle.load(file)
    file.close()

    df = df[tickers].dropna()
    valid_dates = pd.to_datetime(df.index)
    start = valid_dates[0]
    end = valid_dates[-1]

    if time_span == 'years':
        dates = [start.strftime('%Y-%m-%d')]
        curr_date = start
        one_year_from_end = end - relativedelta(years=1)

        while curr_date <  one_year_from_end:
            curr_date += relativedelta(years=1)
            while curr_date not in valid_dates:
                curr_date += relativedelta(days=1)
            dates.append(curr_date.strftime('%Y-%m-%d'))

    elif time_span == 'months':
            dates = []
            curr_date = end - relativedelta(years=2, months = 3)
            while curr_date <  end:
                curr_date += relativedelta(months=3)
                while curr_date not in valid_dates:
                    curr_date += relativedelta(days=1)
                    if curr_date > end:
                        break
                if curr_date < end:
                    dates.append(curr_date.strftime('%Y-%m-%d'))

    elif time_span == 'years_shorter':
        dates = [start.strftime('%Y-%m-%d')]
        curr_date = start
        two_years_from_end = end - relativedelta(years=2)

        while curr_date <  two_years_from_end:
            curr_date += relativedelta(years=2)
            while curr_date not in valid_dates:
                curr_date += relativedelta(days=1)
            dates.append(curr_date.strftime('%Y-%m-%d'))

    else:
        raise ValueError('time_span must be "years", "months" or "years_shorter"')

    combos = [(start, end) for start, end in combinations(dates, 2) if start < end]

    return combos