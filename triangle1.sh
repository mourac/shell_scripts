#!/bin/bash
STR="*"
for ((i=1; i<=5; i++))
do
	for ((j=1; j<=i; j++))
	do
		printf "$STR";
	done
	printf "\n";
	
done
