#!/bin/bash

rm dptable.html
rm dptable.csv
python get_packet.py 
csv2html -o dptable.html --table 'class="dptable"' --tr 'class="tr-collapsed"' dptable.csv
sed -i '2 s/\(^.*$\)/<thead>\1<\/thead>/' dptable.html
python format_packet.py

git reset
git add draft-packet.html
git commit -m"update table"
git push origin test-packet
