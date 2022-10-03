#!/usr/bin/perl
use strict;
use CGI qw/param/;

my $change = param("change");

#print "Content-Type: text/plain\n\n";

my $baseSettings = "";
my $newSettings = "";
open(SETTINGS, "/opt/blt/etc/blt-settings.conf");
while (<SETTINGS>) {
    my $line = $_;
    $baseSettings .= $line;
    if (param("newHOST") =~ /./) { my $n = param("newHOST"); $line =~ s/^HOST=.*/HOST="=== $n ==="/g; }
    if (param("newCALIB") =~ /./) { my $n = param("newCALIB"); $line =~ s/^CALIB=.*/CALIB=$n/g; }
    if (param("newTOD") =~ /./) { my $n = param("newTOD"); $line =~ s/^TOD=.*/TOD=$n/g; }
    if (param("newCARD") =~ /./) { my $n = param("newCARD"); $line =~ s/^CARD=.*/CARD=$n/g; }
    if (param("newMODE") =~ /./) { my $n = param("newMODE"); $line =~ s/^DEVICEMODE=.*/DEVICEMODE=$n/g; }
    if (param("newDEVICE") =~ /./) { my $n = param("newDEVICE"); $line =~ s/^DEVICE=.*/DEVICE=$n/g; }
    $newSettings .= $line;
}
close(SETTINGS);
#print "OK: $change\n";
#print "=========== FROM ===========\n";
#print $baseSettings;
#print "=========== TO ===========\n";
#print $newSettings;

open(NSF, ">/opt/blt/etc/blt-settings.conf");
print(NSF $newSettings);
close(NSF);

if (param("restartread") == 1) {
    #print "RESTART READ\n";
    `sudo /usr/sbin/service blt-read restart`;
}
if (param("restartgen") == 1) {
    #print "RESTART GEN\n";
    `sudo /usr/sbin/service blt-gen restart`;
}

print "Location: settings.cgi\n\n";
