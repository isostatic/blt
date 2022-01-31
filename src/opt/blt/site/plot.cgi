#!/bin/bash 
. /opt/blt/etc/blt-settings.conf
echo "Content-type: image/png"
echo ""

TMP="$WORKDIR/dt.log"
cat `find $WORKDIR -mmin -600 -name 2*.log` |grep ^INFO:.2|cut -d ' ' -f 2,3,8,16 |sed -e 's/ /T/'|sort|tail -4000 > $TMP
gnuplot -c /opt/blt/bin/plot.gp
rm $TMP
