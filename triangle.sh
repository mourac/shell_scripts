#!/bin/bash
STR="*"
for ((i=1; i<=5; i++))
do
	echo "$STR"
	STR="$STR *"
done
