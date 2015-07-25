; row++))
do
        for ((spaces=row;spaces>=NUMBER;spaces--))
        do
                echo -ne " "
        done
        for ((i=1;i>=row; i--))
        do
                echo -ne "$STR"
        done
        echo

