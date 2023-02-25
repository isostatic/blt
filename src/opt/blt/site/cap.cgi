#!/bin/bash
. /opt/blt/etc/blt-settings.conf
echo "Content-type: image/jpeg"
echo ""
CURPCM=${CURYUV/yuv/pcm}
/opt/blt/bin/ffmpeg -f rawvideo -vcodec rawvideo -pix_fmt uyvy422 -s 1920x1080 -r 25 -i $CURYUV  -f s16le -acodec pcm_s16le -ar 48000 -ac 2  -i $CURPCM -filter_complex "[1]showwaves=split_channels=1:mode=cline:scale=$GTYPE:s=1920x1080[vol];[0]scale=1920:1080[sc];[sc][vol]overlay=0:main_h-overlay_h" -y -f mjpeg - 2>/dev/null
