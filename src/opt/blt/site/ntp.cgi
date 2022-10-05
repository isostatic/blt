#!/usr/bin/perl
use strict;
use CGI qw/param/;

my $ntpSvr = "pool.ntp.org";
open(SETTINGS, "/opt/blt/etc/blt-settings.conf");
while (<SETTINGS>) {
	if (/^NTP_SVR=(.*)$/) {
		$ntpSvr = $1;
	}
}
close(SETTINGS);

my $cmd = "ntpdate -q $ntpSvr";
if (param("forceSync") == 1) {
	$cmd = "sudo /opt/blt/bin/forceSync.sh";
}

my $res = "Failure checking NTP server $ntpSvr";
open(F, "$cmd|");
while (<F>) {
   if (/time server ([^ ]*) offset ([\-0-9\.]*)/) {
        my $svr = $1;
        my $sec = $2;
        my $ms = $2 * 1000;
        my $frame = int($ms / 40);
        if ($frame == 0) {
            $res = "<b>Correctly synced</b>";
        } else {
            $res = "<b>$frame frames off</b>";
        }
	if ($sec < 1) {
		$sec = $sec*1000;
		$sec .= "m";
	}
        $res .= "<small>:${sec}s (${frame} frame) offset, according to $svr</small>";
   }
}
close(F);
print "Content-Type: text/plain\n\n";
print "$res";
