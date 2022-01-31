#!/bin/bash
#sudo apt install gnuplot-nox expect apache2 tesseract-ocr

sudo ln -fs /opt/blt/etc/blt-gen.service /etc/systemd/system/ && sudo systemctl daemon-reload
sudo ln -fs /opt/blt/etc/blt-read.service /etc/systemd/system/ && sudo systemctl daemon-reload
sudo systemctl start blt-gen.service
sudo systemctl start blt-read.service

sudo ln -fs /opt/blt/etc/blt-snapshot-cron /etc/cron.d/

sudo ln -fs /opt/blt/etc/blt-site /etc/apache2/sites-enabled/blt-site.conf
if [[ -e /etc/apache2/mods-enabled/cgid.conf ]]
then
    sudo service apache2 reload
else 
    sudo /usr/sbin/a2enmod cgi
    sudo service apache2 restart
fi

sudo chmod 777 /opt/blt/work/
