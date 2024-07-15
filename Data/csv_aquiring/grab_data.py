
"""
grab_data.py
Purpose: grab data from Yahoo! Finance and store it in a csv.
Inputs: ticker name as a string
Outputs: .csv file containing daily stock price for that ticker
"""
import yfinance as yf
import pandas as pd
import sys

def grab_data(ticker_name):
    ticker = yf.Ticker(ticker_name.upper())
    hist = ticker.history(period="max")["Close"]
    csv_hist = hist.to_csv()
    # print(csv_hist) #i like using pipes hehe
    with open(f"{ticker_name}.csv", "w") as file: 
       file.write(csv_hist)


def main():
    grab_data(sys.argv[1]) #Take ticker as argument


if __name__ == "__main__":
    main()
