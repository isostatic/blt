set terminal png
set xdata time
set timefmt "%Y-%m-%dT%H:%M:%S"
set format x "%a\n%H:%M"
set key off
set xlabel "Time"
set ylabel "Audio Delay (ms)" tc rgb "#0000FF"
set y2label "Video Latency (frames)" tc rgb "#FF0000"
set autoscale y
set y2range [0:50] 
set y2tics
set autoscale x
# Values beyond half a second out of sync are ridiculous so ignore them

plot "/opt/blt/work/dt.log" \
     using 1:($2 > -24000 && $2 < 24000 ? $2/48 : 1/0) lt rgb "#0000FF", \
  "" using 1:3 axes x1y2 lt rgb "#FF0000"


