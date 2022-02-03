#!/bin/bash 
. /opt/blt/etc/blt-settings.conf
echo "Content-type: image/png"
#echo "Content-type: text/plain"
echo ""
START=4000
NUM=4000
if [[ "$QUERY_STRING" =~ start=([0-9]+) ]]
then
 START=${BASH_REMATCH[1]}
fi
if [[ "$QUERY_STRING" =~ num=([0-9]+) ]]
then
 NUM=${BASH_REMATCH[1]}
fi

TMP="$WORKDIR/dt.log"
#cat `find $WORKDIR -mmin -600 -name 2*.log` |grep ^INFO:.2|cut -d ' ' -f 2,3,8,16 |sed -e 's/ /T/'|sort|tail -4000 > $TMP
cat `find $WORKDIR -mmin -600 -name 2*.log` |grep ^INFO:.2|cut -d ' ' -f 2,3,8,16 |sed -e 's/ /T/'|sort|tail -$START|head -$NUM > $TMP
#echo "START $START"
#echo "NUM $NUM"
#head -1 $TMP
#wc -l $TMP
#tail -1 $TMP
gnuplot -c /opt/blt/bin/plot.gp
rm $TMP
