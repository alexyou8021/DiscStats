#!/bin/sh

python scrape.py

if [ 1 = 1 ]; then
  email_list=alexyou8021@gmail.com
else 
  email_list=reesemb1@gmail.com 
fi

echo "HI REESE" | mailx -s "SHEETES" -a tuff.xls ${email_list}

rm tuff.xls
