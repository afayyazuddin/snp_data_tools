#!/usr/bin/env bash
mkdir ./files

# Make file called with filenames.txt that contains the opensnp
# zip file that contains snp files for each phenotype
# followed by the phenotype (tab-separated).
# The following code reads each filename ($name) and unzips it into a
# directory with the name of the phenotype ($target).
while read line
do
	name=$(echo $line|awk -F '[\/ \t]' '{print "./" $6}')
	target=$(echo $line|awk -F '[\/ \t]' '{print "./files/" $7}')
	unzip $name -d $target
done <filenames.txt

cd ./files

# The following code recursively traverses each subdirectory
# in ./files2 and counts the number of lines of each file and
# appends it to a file called file_list.txt
find . -type f -exec wc -l {} + >> file_list.txt
