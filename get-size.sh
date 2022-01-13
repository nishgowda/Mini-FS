#!/bin/bash

dir=$1
cd $dir
arr=($(ls))
total=0

for i in "${arr[@]}"
do
	size=$(stat -c%s "$i")
	total=$(( total+size ))
#	echo "$i: $size bytes"
done
#echo "the files in $dir have a total of $total bytes"
echo $total

