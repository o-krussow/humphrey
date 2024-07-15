from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate_year_dif(date_str1, date_str2):
    # Convert strings to datetime.date objects
    date1 = datetime.strptime(date_str1, "%Y-%m-%d").date()
    date2 = datetime.strptime(date_str2, "%Y-%m-%d").date()

    # Calculate the difference using relativedelta
    delta = relativedelta(date2, date1)

    # Get the difference in years
    total_years = delta.years
    if total_years == 0:
        return delta.months / 12
    else:
        return total_years