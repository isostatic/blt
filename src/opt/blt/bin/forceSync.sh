#!/bin/bash 
set -e
NTP_SVR=pool.ntp.org

. /opt/blt/etc/blt-settings.conf

ntpdate $NTP_SVR

