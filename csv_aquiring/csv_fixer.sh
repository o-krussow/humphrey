#!/bin/bash

for csvfile in ./pre_csvs/*;
do
cat $csvfile | 
  cut -d',' -f2 |
  paste -d',' <(cat $csvfile | 
  cut -d',' -f1 |
  cut -d' ' -f1) - > ./csvs/$(basename $csvfile)
done
