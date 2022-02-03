#!/usr/bin/perl
use strict;
use CGI qw/param/;
print "Content-Type: text/html\n\n";
my $settings = {};
open(SETTINGS, "/opt/blt/etc/blt-settings.conf");
while (<SETTINGS>) {
    if (/([^=]*)=(.*)/) {
        $settings->{$1} = $2;
    }
}
close(SETTINGS);
#use Data::Dumper; print Dumper $settings; exit 0;
my $SET_yuv = $settings->{CURYUV};
my $SET_log = $settings->{CURLOG};
my $SET_detdec = $settings->{DETDEC};

my @s = stat($SET_yuv);
my $age = time() - @s[9];
my $name = `hostname`;

my $frozenwarn = "";
if ($age > 30) {
    $frozenwarn = "frozen";
}

open(L, "tail $SET_log|");
my $out = "";
while (<L>) {
    # INFO: 2022-01-27 16:47:57 GMT> Current audio delay 373 samples (7 ms). Current Calibrated Video Latency 8 frames (6). 
    if (/INFO: (....-..-.. ..:..:.. ...)> Current audio delay ([-0-9]+) samples.*Current Calibrated Video Latency ([0-9]+) frames \(([0-9]+)\)/) {
        my $totVid = $3 + $4;
        my $audioMS = int($2 / 48);
        my $lead = "leading";
        if ($audioMS > 0) { $lead = "trailing"; }
        $out = "At $1, audio is $lead by <b>${audioMS}ms</b> ($2 samples). <br>";
        $out .= "Video latency calculated at $totVid, with a built in calibration of $4 frames meaning latency = <b>$3 frames</b>, but this relies on various factors.<br>";
    }
}
close(L);

open(DD, $SET_detdec);
my $curDec = "";
my $decChange = "";
while (<DD>) {
    my ($dte, $dec) = split(/ /);
    $dec =~ s/\s*$//;
    $dec =~ s/^i//; # Sometimes the decoder outputs an i at the start
    next if ($dec !~ /[a-zA-Z]/); # Decoder failed to decode
    if ($dec ne $curDec) {
        $dte =~ s/T/ /;
        $dte =~ s/\+/ +/;
        $dte =~ s/\-/ -/;
        $decChange .= "$dte switch from '$curDec' to '$dec'<br>";
        $curDec = $dec;
    }
}
close(DD);

my $start = param("start") || 4000;
my $num = param("num") || 4000;
my $lstart = $start + 2000;
my $rstart = $start - 2000;
if ($rstart < 2000) { $rstart = 2000; }

my $lnum = $num + 2000;
my $rnum = $num - 2000;
my $zlstart = $start;
my $zrstart = $start;
if ($zlstart < $lnum) { $zlstart = $lnum; }

print <<EOF
<html>
<head>
<link href="style.css" rel="stylesheet" />
</head>
<body>
<h1>Broadcast Latency Tester</h1>
<h2> $name</h2>
<div class='preview'> 
<img src='cap.cgi'> 
<div class='title $frozenwarn'>Current screenshot $age seconds ago</div>
</div>
<div class='graph'> 
<img src='plot.cgi?start=$start&num=$num'> 
<div class='title'><a href='index.cgi?start=$lstart&num=$num'>&lt;</a><a href='index.cgi?start=$zlstart&num=$lnum'>-</a>  Recent audio offset  <a href='index.cgi?start=$zrstart&num=$rnum'>+</a><a href='index.cgi?start=$rstart&num=$num'>&gt;</a></div>
</div>

<div class='log'>
$out
</div>
<div class='dechist'>
$decChange
</div>
<p>
This latency tester generates a signal using FFMPEG out of a Blackmagic video card, which has a frame counter burnt into the output<br>

Full details on its purpose and use are <a href='Readme.html'>in the readme</a>
</body></html>

EOF
;
