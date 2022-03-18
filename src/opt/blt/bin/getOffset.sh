#!/bin/bash
NTPSYNC=0
OFFSET=0

if [ -x /usr/bin/timedatectl ]
then
CANNTP=0
timedatectl show|grep -q CanNTP=yes && CANNTP=1
timedatectl show|grep -q NTPSynchronized=yes && NTPSYNC=1
if [[ $CANNTP == 1 ]]
then
	if [[ $NTPSYNC == 0 ]]
	then
		echo "ERROR: Not NTP Synced via tiemdatectrl"
		exit 2;
	fi
fi
fi

if [ -x /usr/sbin/ntpdate ]
then    
SEC=`ntpdate -q pool.ntp.org|grep ntpdate|sed -e 's/.*offset //' -e 's/ sec//'`
US=`echo "$SEC * 1000000" | bc | sed -e 's/\..*//'`
if [[ "$US" -lt 20000 ]]
then
if [[ "$US" -gt -20000 ]]
then
	NTPSYNC=1
	OFFSET=$US
fi
fi
fi

if [[ $NTPSYNC == 0 ]]
then
	echo "ERROR: Not NTP Synced - ${OFFSET}us off"
	exit 2
fi
if [[ "$OFFSET" == "x" ]]
then
echo "NTP Synced"
else
echo "NTP Synced (${OFFSET}us)"
fi

