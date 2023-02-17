#!/usr/bin/perl
use strict;
use CGI qw/param/;
use POSIX qw/strftime/;
my $settings = {};
open(SETTINGS, "/opt/blt/etc/blt-settings.conf");
while (<SETTINGS>) {
    if (/([^=]*)=(.*)/) {
        $settings->{$1} = $2;
    }
}
close(SETTINGS);
#use Data::Dumper; print Dumper $settings; exit 0;
#print "Content-Type: text/plain\n\n";

my $_note = param("note");

my $note = "";
$_note =~ s/[^A-Za-z0-9_'\. -]//g;
if ($_note =~ /([A-Za-z0-9_\.' -]+)/) {
    $note = $1;
}

my $SET_detdec = $settings->{DETDEC};
my $date = strftime("%Y-%m-%dT%H:%M:%S%z", localtime);

my $line = "$date NOTE: $note\n";
#print "Passed note: $_note\n";
#print "Sanitised note: $note\n";
#print "Adding note: $line\n";

open(NTE, ">>$SET_detdec") || print "Can't Add Note\n";
print(NTE $line);
close(NTE);


print "Location: index.cgi\n\n";
