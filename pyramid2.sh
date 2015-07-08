n=$1;
for((i=1;i<=n;i++))
do
	for ((k=i;k<=n;k++))
	do
		echo -ne " ";
	done
	for ((j=1;j<=2*i-1;j++))
	do
		echo -ne "*"
	done
echo;
done
