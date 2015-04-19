#!/usr/bin/env python3.4

"""
	sudo ipset create banthis hash:ip maxelem 1000000
	sudo ipset add banthis 1.1.1.1
	sudo iptables -I INPUT -m set --match-set banthis src -p tcp --destination-port 22 -j DROP


	$ sudo ipset save banthis > banthis.txt
	$ sudo ipset destroy banthis
	$ sudo ipset restore -f banthis.txt

"""

# IMPORTS
import hashlib
import re
import socket
import pprint
import subprocess
import commands
import os
import time

# VARS
log_path = '/var/log/auth.log'
hosts=[]
full_hosts_data=[]
previous_ip = ""
previous_host = ""

#Create ipset
def create_banthis():
	return subprocess.call("ipset create banthis hash:ip maxelem 1000000" ,shell=True);

#Save ipset
def save_banthis():
	return subprocess.call("ipset save banthis > banthis.txt" ,shell=True);

#Add ip to ipset
def anhade_ip(ip):
	return subprocess.call(["ipset", "add", "banthis", ip]);

#Add ipset to iptables
def anhade_iptables():
	subprocess.call("iptables -I INPUT -m set --match-set banthis src -p tcp --destination-port 22 -j DROP",shell=True);

def borra_iptables():
	p = subprocess.Popen(["iptables", "-L", "--line-numbers"], stdout=subprocess.PIPE);
	output , err = p.communicate();
	for line in output.split("\n"):
		check_1 = line.find("banthis");
		if check_1 != -1 :
			index= subprocess.call("iptables -D INPUT " + line[0],shell=True);

#Check requirements
def check_requirements():
  ipset_status = commands.getstatusoutput("hash ipset")
  iptables_status = commands.getstatusoutput("hash iptables")
  if ipset_status[0] != 0 or iptables_status[0] != 0:
    raise Exception("Iptables and/or ipset not found, please intstall these dependencies first")

#Adjust lines
def adjust_item( str, i ):
    if len(str) < i:
        for j in range(i-len(str)):
            str = str + " "
    return str

#Lookup ip by name
def get_ip_hostname(name):
	try:
            return socket.gethostbyname(name);
        except Exception:
            return "0";

#Date
def get_date( my_line ):
    date_words = my_line.split(":")
    date = date_words[0] +":"+ date_words[1] +":"+ ((date_words[2]).split(" "))[0]
    return date

try:
	start_time = time.time();
	check_requirements();
	if save_banthis() == 1:
		create_banthis();

	# READ FILE
	with open(log_path, 'rt') as log:
		   text = log.read();

	# COLLECTING HOSTS AND IPS
	for line in text.split("\n"):
		if "sshd" in line:
			if len(line) > 5:
				check_1 = line.find("rhost=")
				if check_1 != -1 :
					words = line[check_1:len(line)].split(" ");
					if len(words) > 2 :
						if len(words[2]) > 5 :
							user = words[2].split("=")[1];
							ip = words[0].split("=")[1];
							host = ip;
							pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$");
							test = pat.match(ip);
							if not test:
								ip = get_ip_hostname(ip);
								if ip != "0":
									host = ip;
							exists_check = 0
							for my_host in hosts:
								if my_host["ip"] == ip:
									exists_check = 1;
							if exists_check == 0:
								if not "192.168." in ip :
									hosts.append({"ip":ip, "hostname":host , "accounts":user, "date":get_date( line )});

	# PRINT TABLE HEADERS
	print(
		adjust_item("DATE", 16 ),
		adjust_item("IP", 15),
		adjust_item("HOSTNAME", 40),
		adjust_item("ACCOUNTS", 30)
	)
	for item in hosts:
		anhade_ip(item["ip"])
		parsed_ip           = adjust_item( item["ip"],          15 )
		parsed_date         = adjust_item( item["date"],        16 )
		parsed_host         = adjust_item( item["hostname"] ,   40 )
		parsed_accounts     = adjust_item( item["accounts"],    30 )
		print(
			parsed_date[:16],
			parsed_ip, parsed_host[:40],
			parsed_accounts[:30],
		)
	borra_iptables();
	anhade_iptables();
	print("--- %s seconds ---" % (time.time() - start_time));
except Exception as e:
	print str(e);
