#!/bin/bash 
DETDEC=/opt/blt/work/detected_decoder.log
. /opt/blt/etc/blt-settings.conf

echo "`date -Is` NOTE: $@" >> $DETDEC
