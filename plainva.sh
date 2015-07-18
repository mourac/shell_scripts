#!/bin/bash
a=23
echo $a
b=$a
echo $b

a='echo Hello!'
echo $a

a='ls -l'
echo $a
echo 
echo "$a"
exit 0
R=$(cat /etc/redhat-release)
arch=$(uname -m)
