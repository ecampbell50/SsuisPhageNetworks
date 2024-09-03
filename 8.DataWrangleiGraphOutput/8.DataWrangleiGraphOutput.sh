#!/bin/bash

read -p "Enter the file name of the iGraph output from 5.GetCommunityIDs.py:" input_file
read -p "Are these bacterial or prophage genomes? " TAG
edgetable=$(basename $input_file)

# Change the output of igraph to something usable
cat "$input_file" | sed 's/Community /Community_/g' | sed 's/\: \[/,/g' | sed 's/ //g' | sed 's/\]//g' | sed "s/'//g" > "${edgetable}_AllCommunities.txt"

# Get each community list in a file of it's community name
for i in $(cat "${edgetable}_AllCommunities.txt");
do
	echo ${i#*,} > ${i%%,*}_${TAG}.csv
done

# Replace all commas in the new files as a new line
for j in Community*${TAG}.csv;
do
	sed -i 's/,/\n/g' $j
done

# Get a list of every ID and the community it belongs to
touch MembersToCommunity.csv
echo "ID,Community" >> MembersToCommunity.csv

for x in Community*.csv;
do
	for y in $(cat "${x}");
	do
		echo "$y,${x%.csv}" >> MembersToCommunity.csv
	done
done
