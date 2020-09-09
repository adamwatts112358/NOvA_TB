#!/bin/bash

# merge_output.sh
# Mike Wallbank
#
# Usage: merge_output.sh /path/to/files/ [option]
# When no option is specified, the related files in each subdirectory are merged
# When option 'all' is specified, the merged files in each subdirectory are merged into the final output in the specific directory

if [ "$#" -ne 1 ] && [ "$#" -ne 2 ]; then
    echo "Useage: merge_output.sh /path/to/files/ [option]"
    exit
fi

if [ "$2" = "all" ]; then
    for det in $(seq 28 28); do
	echo "Merging detector $det files into $1/${det}_all.txt"
	touch $1/${det}_all.txt
	chmod +w $1/${det}_all.txt
	cat $1/*/${det}_all.txt > $1/${det}_all.txt
    done
else
    for dir in `ls $1`; do
	for det in $(seq 28 28); do
	    echo "Merging detector $det files into $1/${dir}/${det}_all.txt"
	    touch $1/${dir}/${det}_all.txt
	    chmod +w $1/${dir}/${det}_all.txt
	    cat $1/${dir}/${det}_*.txt > $1/${dir}/${det}_all.txt
	done
    done
fi