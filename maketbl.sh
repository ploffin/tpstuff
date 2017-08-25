#!/bin/bash

all_csv_str=$( echo "*.csv" | sort )
all_csv=( $all_csv_str )

csv2html -o dptable.html -r --table 'class="dptable"' --tr 'class=tr-collapsed' "${all_csv}"

echo "document.write('$(cat dptable.html | sed 's/\x27/\&quot;/g' | tr '\n' ' ' )');" > dptable.js
