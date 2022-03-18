#!/bin/bash 
set -e
FRAMES=600
NAME=appapp
. /opt/blt/etc/blt-settings.conf

DATE=`date +"%Y%m%d-%H%M%S"`
TMPDIR=`mktemp -d `
SUBDIR="$DATE-$NAME"
mkdir -p $TMPDIR/$SUBDIR

SECS=$(($FRAMES/25))

sudo systemctl stop blt-read.service
chmod 666 $WORKDIR/current.yuv
/opt/blt/bin/ffmpeg -f lavfi -i "smptehdbars=rate=50:size=1920x1080" -an -filter_complex "tinterlace=interleave_top,fieldorder=tff,drawtext=text='BLT Currently Capturing for $SECS seconds':x=(w-tw)/2:y=300:fontsize=48:fontcolor=white:box=1:boxcolor=black" -acodec pcm_s16le -pix_fmt uyvy422 -s 1920x1080 -r 25 -t 0.04 -y $WORKDIR/current.yuv
chmod 666 $WORKDIR/current.yuv
/opt/blt/bin/BLT -d $DEVICE -m $DEVICEMODE -n $FRAMES -v $TMPDIR/$NAME.yuv -a $TMPDIR/$NAME.pcm
/opt/blt/bin/ffmpeg -f lavfi -i "smptehdbars=rate=50:size=1920x1080" -an -filter_complex "tinterlace=interleave_top,fieldorder=tff,drawtext=text='BLT Capture complete, restarting':x=(w-tw)/2:y=300:fontsize=48:fontcolor=white:box=1:boxcolor=black" -acodec pcm_s16le -pix_fmt uyvy422 -s 1920x1080 -r 25 -t 0.04 -y $WORKDIR/current.yuv
chmod 666 $WORKDIR/current.yuv
sudo systemctl start blt-read.service

#/opt/blt/bin/ffmpeg -f rawvideo -vcodec rawvideo -pix_fmt uyvy422 -s 1920x1080 -r 25 -i $TMPDIR/$NAME.yuv -f s16le -acodec pcm_s16le -ar 48000 -ac 2 -i $TMPDIR/$NAME.pcm -y $TMPDIR/$NAME.mov

/opt/blt/bin/ffmpeg -f rawvideo -vcodec rawvideo -pix_fmt uyvy422 -s 1920x1080 -r 25 -i $TMPDIR/$NAME.yuv -f s16le -acodec pcm_s16le -ar 48000 -ac 2 -i $TMPDIR/$NAME.pcm -y -vcodec libx264 $TMPDIR/$NAME.m4v \
-filter_complex \
"
[1]showwaves=split_channels=1:mode=line:s=1920x200[vol];
[0][vol]overlay=10:main_h-overlay_h-10
"


/opt/blt/bin/ffmpeg -f rawvideo -vcodec rawvideo -pix_fmt uyvy422 -s 1920x1080 -r 25 -i $TMPDIR/$NAME.yuv -f s16le -acodec pcm_s16le -ar 48000 -ac 2 -i $TMPDIR/$NAME.pcm -y -vcodec mjpeg \
-filter_complex \
"
[1]showwaves=split_channels=1:mode=line:s=1920x200[vol];
[0][vol]overlay=10:main_h-overlay_h-10
" \
$TMPDIR/$SUBDIR/%04d.jpg


cd $TMPDIR/$SUBDIR
mv "$TMPDIR/$NAME.m4v" "$TMPDIR/$SUBDIR/"
echo "
<html>
<body>
Recording of $NAME at $DATE<br>
<video width='640' height='360' controls><source src='$NAME.m4v' type='video/mp4'></video><br><br>" >> index.html
for I in *jpg
do echo "<img title='$I' width='384' height='216' src='$I'>" >> index.html
done
mv $TMPDIR/$SUBDIR /opt/blt/site/

echo /opt/blt/site/$SUBDIR 

rm -f /opt/blt/site/latestRecording
ln -fs  /opt/blt/site/$SUBDIR /opt/blt/site/latestRecording

#rm -rf $TMPDIR
