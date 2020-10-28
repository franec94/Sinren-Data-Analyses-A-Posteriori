#!/usr/bin/env perl
# export PERL5LIB=/c/Strawberry/perl/vendor/lib:/c/Strawberry/perl/site/lib

use warnings;
use strict;
use utf8;

use Getopt::ArgParse;
use Text::CSV;
use Text::Tabulate;
use Text::Table;
use Data::Dumper;

binmode STDOUT, ':encoding(utf8)';

my $ap = Getopt::ArgParse->new_parser(
       prog        => 'A perl script',
       description => 'This is a program for testing perl usage',
   epilog      => 'This program is intended for practice perl',
);

# Parse an option: '--file_path value' or '-f value'
$ap->add_arg('--file_path', '-f', dest => 'file_path');
# Parse a boolean: '--bool' or '-b' using a different name from
# the option
$ap->add_arg('--show_as_table', type => 'Bool', dest => 'show_as_table');

my $namespace = $ap->parse_args(@ARGV);
printf("Input file: %s\n", $namespace->file_path);
printf("Show as table: %s\n", $namespace->show_as_table);

my $csv = Text::CSV->new({ sep_char => ',' });
open(my $data, '<', $namespace->file_path) or die "Could not open '$namespace->file_path' $!\n";

my @cols = qw/____Date____ ____Timestamp____ Hidden_Features Hidden_Layers Trials_no./;
my $sep = \'│';
 
my $major_sep = \'║';
my $tb  = Text::Table->new( $sep, " Number ", $major_sep,
    ( map { +( ( ref($_) ? $_ : " $_ " ), $sep ) } @cols ) );
 
my $num_cols = @cols;
 
my $make_rule = sub {
    my ($args) = @_;
 
    my $left      = $args->{left};
    my $right     = $args->{right};
    my $main_left = $args->{main_left};
    my $middle    = $args->{middle};
 
    return $tb->rule(
        sub {
            my ( $index, $len ) = @_;
 
            return ( '─' x $len );
        },
        sub {
            my ( $index, $len ) = @_;
 
            my $char = (
                  ( $index == 0 )             ? $left
                : ( $index == 1 )             ? $main_left
                : ( $index == $num_cols + 1 ) ? $right
                :                               $middle
            );
 
            return $char x $len;
        },
    );
};
 
my $start_rule = $make_rule->(
    {
        left      => '┌',
        main_left => '╥',
        right     => '┐',
        middle    => '┬',
    }
);
 
my $mid_rule = $make_rule->(
    {
        left      => '├',
        main_left => '╫',
        right     => '┤',
        middle    => '┼',
    }
);
 
my $end_rule = $make_rule->(
    {
        left      => '└',
        main_left => '╨',
        right     => '┘',
        middle    => '┴',
    }
);

my $i = 1;
while (my $line = <$data>) {
  chomp $line;
 
  my @fields = split "," , $line;
  # printf("%s %s\n", $fields[0], $fields[1])
  my @arr = ($i);
  $tb->add((@arr, @fields));
  $i += 1;
}
close $data;
 
print $start_rule, $tb->title,
    ( map { $mid_rule, $_, } $tb->body() ), $end_rule;
