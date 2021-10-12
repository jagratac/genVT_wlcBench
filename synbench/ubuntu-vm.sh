#!/bin/bash
args=("$@")
for((i=0;i<=20;i++));
do
	echo ${args[0]}-$i
done 
