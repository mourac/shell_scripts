#!/bin/bash
##########################################################################################
# Author : Shivaji Thanneeru                                                             #
# Date   : 7/17/2015                                                                     #
# break_tests_into_suites.sh scipt the given file ($1) into given number of files($2)    #
##########################################################################################
if [ $# -ne 2 ]
    then echo Usage: `basename $0` list_of_tests number_of_desired_test_suites
    echo Example : ./break_tests_into_suites.sh tests.txt 2
else
        TESTS_FILE=$1
        DESIRED_TEST_SUITES=$2
        LINES_IN_TESTS=(`wc -l $TESTS_FILE`)
        TESTS_IN_SUITES=`expr $LINES_IN_TESTS / $DESIRED_TEST_SUITES`
        mkdir suites
        split -l $TESTS_IN_SUITES -d  $TESTS_FILE suites/suite
fi
