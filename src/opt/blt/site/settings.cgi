#!/usr/bin/perl
use strict;
print "Content-Type: text/plain\n\n";


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

my $devs = listDevices();
use Data::Dumper;
#print Dumper $devs;

#print Dumper $devs;

foreach my $id (keys %{$devs->{id}}) {
    my $name = $devs->{id}->{$id};
    print "$id: [$name]\n";
    my $modes = listDeviceById($id);
    foreach my $modeID (keys %{$modes->{id}}) {
        my $modeName = $modes->{id}->{$modeID}->{name};
        print " $modeName\n";
    }
}
