#!/bin/bash
ps -fe|grep web_run |grep -v grep
if [ $? -ne 0 ]
then
echo "start process....."
cd /root/projects/anirec
source py35/bin/activate
python web_run.py
else
echo "runing....."
fi
