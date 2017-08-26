#!/bin/bash

python get_packet.py 
csv2html -o dptable.html -r --table 'class="dptable"' --tr 'class=tr-collapsed' dptable.csv
sed -i '2 s/\(^.*$\)/<thead>\1<\/thead>/' dptable.html
echo "document.write('$(cat dptable.html | sed 's/\x27/\&quot;/g' | tr '\n' ' ' )');" > dptable.js
rm dptable.html
rm dptable.csv

git reset
git add dptable.js
git commit -m"update table"
git push origin test-packet
