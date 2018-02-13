#!/bin/sh

#python scrape.py $1 '5630483324993536'
python scrape.py $1 '5686436867080192'

if [ 2 = 2 ]; then
  email_list=alexyou8021@gmail.com
else 
  email_list=reesemb1@gmail.com 
fi

echo "Singlewide Stats" | mailx -s "Team stats!" -a Singlewide.xls ${email_list}

rm Singlewide.xls
