#!/usr/bin/env python
"""
author: K.Draziotis, drazioti@gmail.com
licence : GPL v.2

A simple script that checks your ip every some time interval
and write it to the file ip_file.txt

You can deamonize it, with nohup
$chmod +x ip_python.py
$nohup ./ip_python.py  &>/dev/null 1>&2 &>/dev/null&

"""
import requests
import datetime
import time
day = 3600
time_interval = 10 #in seconds
starttime=time.time()
while True:
	with open("ip_file.txt", "a") as f:
		r = requests.get('http://checkip.dyndns.org').text
		now = datetime.datetime.now()
		f.write(now.isoformat())
		f.write(" : ")
		f.write(r[76:89])
		f.write("\n")
		f.close()
	time.sleep(time_interval - ((time.time() - starttime) % time_interval))
