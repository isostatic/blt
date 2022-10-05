#!/usr/bin/perl
use strict;
use CGI qw/param/;


sub err() {
	print "Content-Type: text/html\n\n";
	print "<html><body>Error writing config file <code>".`ls -l /opt/blt/etc/blt-settings.conf`."</code> -- fix permissions? <br><a href='settings.cgi'>Return to settings</a> </body> </html>";
	exit;
}

my $change = param("change");

#print "Content-Type: text/plain\n\n";

my $baseSettings = "";
my $newSettings = "";
open(SETTINGS, "/opt/blt/etc/blt-settings.conf");
while (<SETTINGS>) {
    my $line = $_;
    $baseSettings .= $line;
    if (param("newCALIB") =~ /./) { my $n = param("newCALIB"); $line =~ s/^CALIB=.*/CALIB=$n/g; }
    if (param("newTOD") =~ /./) { my $n = param("newTOD"); $line =~ s/^TOD=.*/TOD=$n/g; }
    if (param("newCARD") =~ /./) { my $n = param("newCARD"); $line =~ s/^CARD=.*/CARD="$n"/g; }
    if (param("newMODE") =~ /./) { my $n = param("newMODE"); $line =~ s/^DEVICEMODE=.*/DEVICEMODE=$n/g; }
    if (param("newDEVICE") =~ /./) { my $n = param("newDEVICE"); $line =~ s/^DEVICE=.*/DEVICE=$n/g; }
    if (param("newNTP") =~ /./) { my $n = param("newNTP"); $line =~ s/^NTP_SVR=.*/NTP_SVR=$n/g; }

    # optional settings
    if (param("newHOST") =~ /./) { my $n = param("newHOST"); $line =~ s/^HOST=.*/HOST="=== $n ==="/g; }
    if (param("newBACK") =~ /./) { my $n = param("newBACK"); $line =~ s/^BACKGROUND=.*/BACKGROUND=$n/g; }
    $newSettings .= $line;
}
close(SETTINGS);
if ($newSettings !~ /BACKGROUND=/) { if (param("newBACK") =~ /./) { my $n = param("newBACK"); $newSettings .= "BACKGROUND=$n\n"; } }
if ($newSettings !~ /HOST=/) { if (param("newHOST") =~ /./) { my $n = param("newHOST"); $newSettings .= "HOST=$n\n"; } }
if ($newSettings !~ /NTP_SVR=/) { if (param("newNTP") =~ /./) { my $n = param("newNTP"); $newSettings .= "NTP_SVR=$n\n"; } }
#print "OK: $change\n";
#print "=========== FROM ===========\n";
#print $baseSettings;
#print "=========== TO ===========\n";
#print $newSettings;

open(NSF, ">/opt/blt/etc/blt-settings.conf") or err();
print(NSF $newSettings);
close(NSF);

my $checkSet = "";
open(SETTINGS, "/opt/blt/etc/blt-settings.conf");
while (<SETTINGS>) {
	$checkSet .= $_;
}
close(SETTINGS);
if ($checkSet ne $newSettings) {
	err();
}


if (param("restartread") == 1) {
    #print "RESTART READ\n";
    `sudo /usr/sbin/service blt-read restart`;
}
if (param("restartgen") == 1) {
    #print "RESTART GEN\n";
    `sudo /usr/sbin/service blt-gen restart`;
}

print "Location: settings.cgi\n\n";
