#!/usr/bin/perl
use strict;
use CGI qw/param/;
sub listDevices() {
    open(LD, "/opt/blt/bin/BLT -h 2>&1|");
    my $in = 0;
    my $devBy = {};
    while (<LD>) {
        if (/device id>:/) { $in = 1; }
        if (/mode id>:/) { $in = 0; }
        if ($in) {
            if (/([0-9]+): (.*)/) {
                $devBy->{name}->{$2} = $1;
                $devBy->{id}->{$1} = $2;
            }
        }
    }
    close(LD);
    return $devBy;
}

sub listDeviceById($) {
    my ($id) = @_;
    open(LD, "/opt/blt/bin/BLT -d $id -h 2>&1|");
    my $in = 0;
    my $modes = {};
    while (<LD>) {
        chomp;
        next if (/Usage/);
        if (/mode id/) { $in = 1; }
        if (/pixelformat/) { $in = 0; }
        if ($in) {
            if (/([-0-9]+): (.*)$/) {
                my $id = $1;
                my ($name, $res, $fps) = split(/\t/, $2);
                $name =~ s/^ +//; $name =~ s/ +$//;
                $res =~ s/^ +//; $res =~ s/ +$//;
                $fps =~ s/^ +//; $fps =~ s/ +$//;
                $modes->{id}->{$id}->{name} = $name;
            }
        }
    }
    close(LD);
    return $modes;
    
}



my $curHost = `hostname`;
my $curTOD = 500;
my $curCALIB = 3;
my $curCARD = "";
my $curDEVICE = "";
my $curMODE = "";

open(SETTINGS, "/opt/blt/etc/blt-settings.conf");
while (<SETTINGS>) {
    if (/^HOST="=== (.*) ==="/) { $curHost = "$1"; next; }
    if (/^TOD=([0-9]*)/) { $curTOD = $1; next; }
    if (/^CALIB=([0-9]*)/) { $curCALIB = $1; next; }
    if (/^CARD=(.*)/) { $curCARD = $1; $curCARD =~ s/"//g; }
    if (/^DEVICE=(.*)/) { $curDEVICE = $1; next; }
    if (/^DEVICEMODE=(.*)/) { $curMODE = $1; next; }
}
close(SETTINGS);

my $bltReader = "Not Found";
my $bltGen = "Not Found";
open(PS, "/bin/ps aux|");
while(<PS>) {
	if (s/.* .opt.blt.bin.BLT/BLT/g) { $bltReader = "Running: <code>$_</code>"; }
	if (/ffmpeg.*Field.rate/) { s/.*ffmpeg /ffmpeg /; s/-an -filter.*uyvy422/ ..... /; $bltGen = "Running: <code>$_</code>"; }
}
close(PS);

print "Content-Type: text/html\n\n";

print <<EOH
<html>
<head>
<link href="style.css?s" rel="stylesheet" />
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.1/jquery.min.js"></script> 
<script src='src.js?w'></script>
</head>
<body>
<h1>Broadcast Latency Tester</h1>
NTP Check: <span class='ntp'>checking NTP...</span><br>
BLT Reader: $bltReader<br>
BLT Generator: $bltGen<br>
<h2>Configuration options</h2>
<form action="doSettings.cgi" method="post">
<table >
<tr><th>Option</th><th>Current Setting</th><th>New Setting</th></tr>
EOH
;

my $devs = listDevices();
my $newGenCard = "<select name='newCARD'>";
foreach my $id (sort keys %{$devs->{id}}) {
    my $name = $devs->{id}->{$id};
    my $sel = "";
    if ($name eq $curCARD) { $sel = "selected"; }
    $newGenCard .= "<option $sel value=\"$name\">$name</option>";
}
$newGenCard .= "</select>";

my $niceCurDevice = $curDEVICE;
my $newReadCard = "<select name='newDEVICE'>";
foreach my $id (sort keys %{$devs->{id}}) {
    my $name = $devs->{id}->{$id};
    my $sel = "";
    if ($id eq $curDEVICE) { $niceCurDevice = $name; $sel = "selected"; }
    $newReadCard .= "<option $sel value=\"$id\">$name</option>";
}
$newReadCard .= "</select>";

my $modes = listDeviceById($curDEVICE);
my $niceMode = $curMODE;
my $newMode = "<select name='newMODE'>";
foreach my $id (sort keys %{$modes->{id}}) {
    my $name = $modes->{id}->{$id}->{name};
    my $sel = "";
    if ($id eq $curMODE) { $niceMode = $name; $sel = "selected"; }
    $newMode .= "<option $sel value=\"$id\">$name</option>";
}
$newMode .= "</select>";

print "<tr><td>Generator Card</td><td>$curCARD</td><td>$newGenCard</td></tr>";
print "<tr><td>Reader Card</td><td>$niceCurDevice</td><td>$newReadCard</td></tr>";
print "<tr><td>Reader Mode</td><td>$niceMode</td><td>$newMode</td></tr>";
print "<tr><td class='settingsubmit' colspan='3'><input type='submit' name='change' value='Save Configuration Settings'></td></tr>";
print "</table>";
print "<input type='hidden' name='restartgen' value='1'><input type='hidden' name='restartread' value='1'>";
print "</form><h2>Calibration Settings</h2>";
print "<form action='doSettings.cgi' method='post'><table> <tr><th>Option</th><th>Current Setting</th><th>New Setting</th></tr>";
print "<tr><td>Generator Calibration</td><td>$curTOD ms</td><td><input name='newTOD' size='5' value='$curTOD'></td></tr>";
print "<tr><td>Reader Calibration</td><td>$curCALIB frames</td><td><input name='newCALIB' size='5' value='$curCALIB'></td></tr>";
print "<tr><td class='settingsubmit' colspan='3'><input type='submit' name='change' value='Save Calibration Settings'></td></tr>";
print "</table>";
print "<input type='hidden' name='restartgen' value='1'><input type='hidden' name='restartread' value='1'>";
print "</form><h2>Operational Settings</h2>";
print "<form action='doSettings.cgi' method='post'><table> <tr><th>Option</th><th>Current Setting</th><th>New Setting</th></tr>";
print "<tr><td>Message</td><td>$curHost</td><td><input name='newHOST' size='50' value='$curHost'></td></tr>";
print "<tr><td class='settingsubmit' colspan='3'><input type='submit' name='change' value='Save Operational Settings'></td></tr>";
print "</table>";
print "<input type='hidden' name='restartgen' value='1'><input type='hidden' name='restartread' value='0'>";
print "</form>";
print "<form action='doSettings.cgi' method='post'>";
print "<input type='hidden' name='restartgen' value='1'><input type='hidden' name='restartread' value='1'>";
print "<input type='submit' name='change' value='Restart BLT'></td>";
print "</form>";

print "</body></html>";
