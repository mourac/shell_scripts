#!/bin/bash
######################################################################################################################
#   Author : Mounica Thanneeru                                                                                       #
#   Date   : 7/21/2015                                                                                               #
#   The script taking the logs.txt file and calculates the average of each phase.                                    #
#   The script to accept an optional parameter for producing results in JSON                                         #
#   For complete information read README                                                                             #
######################################################################################################################
if [ $# -lt 1 ] || [[ ( $# -eq 2 ) && ( $2 != "--format=json" ) ]]
then 
    echo Usage: `basename $0` log_file [optionanl]
    echo Example : `basename $0` logs.txt 
    echo Example : `basename $0` logs.txt --format=json
else
    path=$(pwd)
    CreatedTestUser=$(grep "Created test user" $path/$1 | awk 'BEGIN {total=0;}{total+=$6;}END {print "",total/NR}')
    SettingUpScenario=$(grep "Setting up scenario" $path/$1 | awk 'BEGIN {total=0;}{total+=$6;}END {print "",total/NR}')
    FinishingScenario=$(grep "Finishing scenario" $path/$1 | awk 'BEGIN {total=0;}{total+=$5;}END {print "",total/NR}')
    DeletedTestUser=$(grep "Deleted test user" $path/$1 | awk 'BEGIN {total=0;}{total+=$6;}END {print "",total/NR}')
    CleanupScenario=$(grep "Cleanup scenario" $path/$1 | awk 'BEGIN {total=0;}{total+=$5;}END {print "",total/NR}')
fi

if [ $# -eq 1 ]
then
	echo "----------------------------------------------------"
	echo "					    Average"

	echo "Created Test User			$CreatedTestUser"
	echo "Setting Up Scenario			$SettingUpScenario"
	echo "Finishing Scenario			$FinishingScenario"
	echo "Deleted Test User			$DeletedTestUser"
	echo "Clean Up Scenario			$CleanupScenario"

	echo "----------------------------------------------------"

elif [ $# -eq 2 ] && [ $2 == "--format=json" ]
then
	echo '{"Created Test User": '$CreatedTestUser', "Setting Up Scenario": '$SettingUpScenario', "Finishing Scenario": '$FinishingScenario', "Deleted Test User": '$DeletedTestUser', "Clean Up Scenario": '$CleanupScenario'}' | python -mjson.tool

fi

