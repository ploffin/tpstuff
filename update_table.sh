#!/bin/bash

rm dptable.html
rm dptable.csv
rm responses.csv
python get_packet.py 
csv2html -n -o dptable.html --table 'class="dptable"' dptable.csv
csv2html -o responses.html responses.csv
python format_packet.py

#git reset
#git add draft-packet.html
#git commit -m"update table"
#git push origin master
