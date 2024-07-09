#!/bin/bash

TMPCSVDIR=./pre_csvs

while read -r ticker; 
do
	echo $ticker TO $TMPCSVDIR/$ticker.csv
	python grab_data.py $ticker 2> /dev/null > $TMPCSVDIR/$ticker.csv
done < req_tickers

echo FORMATTING CSVS

for csvfile in $TMPCSVDIR/*;
do
echo $csvfile to ./csvs/$(basename $csvfile)
cat $csvfile | 
  cut -d',' -f2 |
  paste -d',' <(cat $csvfile | 
  cut -d',' -f1 |
  cut -d' ' -f1) - > ./csvs/$(basename $csvfile)
done

rm $TMPCSVDIR/*
