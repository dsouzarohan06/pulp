#!/bin/bash
#title           :check_sync_time.sh
#description     :This script will check how long the sync script is running for.
#author          :Rohan Dsouza
#usage           :bash check_sync_time.sh OR ./check_sync_time.sh
#=================================================================================================================


PID=`sudo ps aux | grep "python /opt/scripts/sync-script.py" | grep -v grep | awk {'print $2'}`

if [ -z "$PID" ]; then
        echo "The sync script is not running now"
        exit 0
        else
        PID_STARTTIME="$(sudo ps -p $PID -o lstart=)"
fi

PID_STARTTIME_EPOCH=`date -d "$PID_STARTTIME" +'%s'`

CURRENT_TIME=$(date +%s)

TIMEDIFF=$(expr $CURRENT_TIME - $PID_STARTTIME_EPOCH)

if [ "$TIMEDIFF" -gt "1800" ]
        then
           echo "Sync script running since $PID_STARTTIME"
           exit 2
        else
           echo "Sync script is running fine"
           exit 0
fi
