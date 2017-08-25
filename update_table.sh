#!/bin/bash

rm dp-spreadsheet.csv
python get_packet.py 
csv2html -o dptable.html -r --table 'class="dptable"' --tr 'class=tr-collapsed' dp-spreadsheet.csv

echo "document.write('$(cat dptable.html | sed 's/\x27/\&quot;/g' | tr '\n' ' ' )');" > dptable.js
rm dptable.html

git reset
git add dptable.js
git commit -m"update table"
git push origin master
