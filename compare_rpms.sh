#!/bin/bash
################################################################################################################################
# Script to compare two rpms that are located at rpm_server:/opt/rpms/
# Date Created : 01/28/2015
# Author : Shivaji Thanneeru
################################################################################################################################
if [ $# -ne 2 ]
    then echo Usage: `basename $0` prod_rpm rpm
    echo Example : compare_rpms.sh conf-RC.01501.002.01.t.1-1.noarch.rpm conf-RC.01501.002.03.t.1-1.noarch.rpm
else
   PROD_RPM=$1
   CURR_RPM=$2
   SUBJECT="Diff of $PROD_RPM and $CURR_RPM"
   EMAIL="build@xxx.com"
   ATTACH_FILE=~/compare_rpms/diff.txt
   mkdir -p ~/compare_rpms/prod_rpm ~/compare_rpms/curr_rpm
   cp /opt/rpms/$PROD_RPM ~/compare_rpms/prod_rpm
   cp /opt/rpms/$CURR_RPM ~/compare_rpms/curr_rpm
   cd ~/compare_rpms/prod_rpm
   rpm2cpio $PROD_RPM | cpio -idmv
   cd ~/compare_rpms/curr_rpm
   rpm2cpio $CURR_RPM | cpio -idmv
   diff -r ~/compare_rpms/prod_rpm ~/compare_rpms/curr_rpm >> $ATTACH_FILE
   mutt  -s "$SUBJECT" -a $ATTACH_FILE -- $EMAIL < /dev/null 
   echo $?
   rm -fr ~/compare_rpms
fi

