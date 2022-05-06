#!/usr/bin/perl
use strict;

my $cmd = "ntpdate -q pool.ntp.org";
my $res = "Failure checking NTP";
open(F, "$cmd|");
while (<F>) {
   if (/adjust time server ([^ ]*) offset ([\-0-9\.]*) sec/) {
        my $svr = $1;
        my $sec = $2;
        my $ms = $2 * 1000;
        my $frame = int($ms / 40);
        if ($frame == 0) {
            $res = "<b>Correctly synced</b>";
        } else {
            $res = "<b>$frame frames off</b>";
        }
        $res .= "<small> - ${sec}s offset, according to $svr</small>";
   }
}
close(F);
print "Content-Type: text/plain\n\n";
print "$res";
