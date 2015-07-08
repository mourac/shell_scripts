#!/bin/bash
NUMBER=$1
STR="* " 
SPACE="      "
for ((row=1; row<=NUMBER; row++))
do
   for ((spaces=row;spaces<=NUMBER;spaces++))
   do
	echo -ne " "
   done
   for ((i=1;i<=row; i++))
   do
	echo -ne "$STR"
   done
   echo
done
