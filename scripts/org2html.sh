#!/usr/bin/bash

ORG_PATH=$1
MD_PATH=$(pwd)/public/html

for file in $ORG_PATH/*.org;
do
	FILE_=$(basename $file)
	OUTPUT_PATH=$MD_PATH/${FILE_%%.*}.html

	pandoc $file -o $OUTPUT_PATH
done

