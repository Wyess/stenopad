#!/usr/bin/env perl

use strict;
use warnings;
use v5.14;

my @first_chars = qw/
    NECR
    ECR
    SECR
    SCR
    SWCR
    NERCR
    ERCR
    SERCR
    SRCR
    SWRCR
    NELCR
    ELCR
    SELCR
    SLCR
    SWLCR
    NECL
    ECL
    SECL
    SCL
    SWCL
    NERCL
    ERCL
    SERCL
    SRCL
    SWRCL
    NELCL
    ELCL
    SELCL
    SLCL
    SWLCL
/;

my @second_chars = qw/
    NE
    E
    SE
    S
    SW
    NER
    ER
    SER
    SR
    SWR
    NEL
    EL
    SEL
    SL
    SWL
/;

for my $first (@first_chars) {
    for my $second (@second_chars) {
        say "guide path_null_@{[lc ${first}]}_@{[lc ${second}]}() {";
        say "    return (0, 0) -- (1, 0);";
        say "}";
        say "";
    }
}
