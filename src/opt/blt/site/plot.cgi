#!/bin/bash 
. /opt/blt/etc/blt-settings.conf
#echo "Content-type: text/plain"
echo "Content-type: image/png"
echo ""
START=4000
if [[ "$QUERY_STRING" =~ start=([0-9]+) ]]
then
 START=${BASH_REMATCH[1]}
fi

TMP="$WORKDIR/dt.log"
cat `find $WORKDIR -mmin -600 -name 2*.log` |grep ^INFO:.2|cut -d ' ' -f 2,3,8,16 |sed -e 's/ /T/'|sort|tail -$START|head -4000 > $TMP
#echo "START $START"
#head -1 $TMP
#wc -l $TMP
#tail -1 $TMP
gnuplot -c /opt/blt/bin/plot.gp
rm $TMP
