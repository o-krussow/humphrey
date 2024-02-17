#!/bin/bash

while read -r ticker; 
do
	python grab_data.py $ticker 2> /dev/null > csvs/$ticker.csv
done < req_tickers
