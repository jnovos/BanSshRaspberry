# BanSshRaspberry
Script in python to ban access to the ssh in RasberryPi <br/>
Spanish version here [http://unpoquitindetodo.blogspot.com.es/2015/04/bloquear-banear-las-ips-de-atacantes-al.html](Spanish%20version%20here%20http://unpoquitindetodo.blogspot.com.es/2015/04/bloquear-banear-las-ips-de-atacantes-al.html) 

----------


You must install the application ipset and iptables :

> 
 1. sudo apt-get update
 2. sudo apt-get install ipset
 3. sudo apt-get install iptables
 
To run the application executes the following command:

> sudo python ssh_proct.py

If you want to execute every day you should be run the following commands:
 

> 
    1. crontab -e
    2. add: 00 01 * * * sudo python ~/scripts/ssh_proct.py > ssh_proct.log
    3. sudo service cron start