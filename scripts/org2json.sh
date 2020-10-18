#!/usr/bin/bash

ORG_PATH=$1
JSON_PATH=$(pwd)/public/json

for file in $ORG_PATH/*.org;
do
	FILE_=$(basename $file)
	OUTPUT_PATH=$JSON_PATH/${FILE_%%.*}.json

	emacs "$file" --batch -l ~/.emacs.d/init.el --eval "(org-export-to-file 'json \"$OUTPUT_PATH\")" &> /dev/null
	python -mjson.tool $OUTPUT_PATH $OUTPUT_PATH.pretty 
	mv $OUTPUT_PATH.pretty $OUTPUT_PATH
done

