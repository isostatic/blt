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
my $genlockState = `/opt/blt/bin/testgenlock`;
$genlockState =~ s/Reference: //;
my $genlockCSS = "";
if ($genlockState =~ /NONE/) { $genlockCSS = "nogenlock"; }
if ($genlockState =~ /Locked/) { $genlockCSS = "genlock"; }
my $genlock = "<span class='$genlockCSS'>Genlock state: $genlockState</span>";

open(L, "tail $SET_log|");
my $out = "";
while (<L>) {
    # INFO: 2022-01-27 16:47:57 GMT> Current audio delay 373 samples (7 ms). Current Calibrated Video Latency 8 frames (6). 
    if (/INFO: (....-..-.. ..:..:.. ...)> Current audio delay ([-0-9]+) samples.*Current Calibrated Video Latency ([0-9]+) frames \(([0-9]+)\)/) {
        my $totVid = $3 + $4;
        my $audioMS = int($2 / 48);
        my $lead = "leading";
        if ($audioMS > 0) { $lead = "trailing"; }
        $out = "At $1, audio is $lead by <b>${audioMS}ms</b> ($2 samples). $genlock<br>";
        $out .= "Video latency calculated at $totVid, with a built in calibration of $4 frames meaning latency = <b>$3 frames</b>, but this relies on various factors.<br>";
    }
}
close(L);

open(DD, "$SET_detdec");
my $curDec = "";
my $decChange = "";
my @lines;
while (<DD>) {
    next unless /([^ ]+) (.*)/;
    my $dte = $1; my $dec = $2;
    $dte =~ s/T/ /;
    $dte =~ s/\+/ +/;
    if ($dec =~ /NOTE: (.*)/) {
        push(@lines, "$dte Manually entered event: $1<br>");
        next;
    }
    $dec =~ s/\s*$//;
    $dec =~ s/^i//; # Sometimes the decoder outputs an i at the start
    next if ($dec !~ /[a-zA-Z]/); # Decoder failed to decode
    if ($dec ne $curDec) {
        push(@lines, "$dte switch from '$curDec' to '$dec'<br>");
        $curDec = $dec;
    }
}
close(DD);

# Show latest 5 events
for (my $i = ($#lines); $i > $#lines-5; $i--) {
    $decChange .= $lines[$i] if ($i);
}

my $start = param("start") || 4000;
my $num = param("num") || 4000;
my $lstart = $start + $num;
my $rstart = $start - $num;
if ($rstart < $num) { $rstart = $num; }

my $lnum = int($num * 1.5);
my $rnum = int(($num+2) / 1.5);
my $zlstart = $start;
my $zrstart = $start;
if ($zlstart < $lnum) { $zlstart = $lnum; }

my @recs;
opendir(D,"/opt/blt/site/");
foreach (readdir(D)) {
	my $dir = $_;
	next unless $dir =~ /^smp-([0-9]{4})([0-9]{2})([0-9]{2})-([0-9]{2})([0-9]{2})([0-9]{2})-(.*)/;
	my $dte = "$1-$2-$3"; my $time = "$4:$5:$6"; my $name = $7;
	push(@recs,"<li><a href='./$dir'>$dte $time $name</a></li>");
}
closedir(D);
my $recordings = "<ul>";
foreach (reverse sort @recs) {
	$recordings .= "$_\n";
}
$recordings .= "</ul>";

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
<form action='makeNote.cgi' method='GET'><input name='note'><input type='submit' value="Add Note"></form>
<p>
<a href='./latestRecording'>Latest recording</a>
$recordings
<a href='doRecording.cgi?e'>Do recording</a>
</p>
<p>
This latency tester generates a signal using FFMPEG out of a Blackmagic video card, which has a frame counter burnt into the output<br>

Full details on its purpose and use are <a href='README.html'>in the readme</a>
</body></html>

EOF
;
