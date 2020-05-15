#!/bin/bash
#this scripts get the most recent from man and relaunches the server
git checkout master
git fetch
git pull --rebase origin master
allpid=$(pgrep -u $USER python)
primary=$(echo "$allpid" |grep -m 1 '[0-9]*')
kill=$(echo "$allpid" |grep -v $primary )
kill -9 $kill
cd ../ && nohup python3 launcher.py --bind 129.3.20.26:12100 launcher:app  >/dev/null 2>&1 &
cd ~/csc480/deployment

#this may not be required.
updaterpid=$(pgrep -u $USER updater.sh)
currpid=$(echo "$updaterpid" |grep -m 1 '[0-9]*')
killscript=$(echo "$updaterpid" |grep -v $currpid )
kill -9 $killscript
#this solution will not update at the same time, will be n seconds from time of execution.
