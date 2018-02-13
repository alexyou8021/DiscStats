#!/bin/sh
#tuff2017 - 5691358622777344
#tuff2018 - 5643419011514368
if [ -z "$1" ]; then
    python scrape.py '5691358622777344' 'statsdontmatter' 'PBJ' 'Warm Up' 'Stanford Invite' 'Sectionals' 'Regionals' 
else
    python scrape.py '5643419011514368' 'statsdontmatter' $1
fi

echo "Excel Generated"

if [ 1 = 2 ]; then
  email_list=alexyou8021@gmail.com
else 
  email_list=reesemb1@gmail.com 
fi

echo "HI REESE" | mailx -s "SHEETES" -a TUFF\ 18.xls ${email_list}
echo "Email sent"

rm TUFF\ 18.xls

