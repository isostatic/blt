#!/bin/bash
. /opt/blt/etc/blt-settings.conf
echo "Content-type: image/jpeg"
echo ""
/opt/blt/bin/ffmpeg -f rawvideo -vcodec rawvideo -pix_fmt uyvy422 -s 1920x1080 -r 25 -i $CURYUV -y -f mjpeg - 2>/dev/null
