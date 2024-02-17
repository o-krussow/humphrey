#!/bin/bash

CSVDIR=./csvs

while read -r ticker; 
do
	echo $ticker TO $CSVDIR/$ticker.csv
	python grab_data.py $ticker 2> /dev/null > $CSVDIR/$ticker.csv
done < req_tickers
