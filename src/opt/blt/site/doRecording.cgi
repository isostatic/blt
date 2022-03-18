#!/bin/bash
#echo "Content-Type: text/plain"
#echo ""

sudo /opt/blt/bin/recordSample.sh > /tmp/recording.txt 2>&1 &
disown %1

sleep 1

echo "Location: /blt"
echo ""
