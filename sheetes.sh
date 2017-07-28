#!/bin/sh

python scrape.py

echo "HI REESE" | mailx -s "SHEETES" -a tuff.xls alexyou8021@gmail.com

rm tuff.xls
