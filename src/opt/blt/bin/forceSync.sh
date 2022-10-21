#!/bin/bash 
set -e
NTP_SVR=pool.ntp.org

. /opt/blt/etc/blt-settings.conf

ntpdate -b -u $NTP_SVR

