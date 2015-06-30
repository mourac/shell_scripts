#!/bin/bash
for ((i=1; i<=10; i++))
do
	echo first loop 
	for ((j=1; j<=$i; j++))
        do
		echo second loop
        done
done


