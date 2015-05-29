#!/bin/sh

# move to target directory
cd ./"TARGET_DIR"
# get file list
file=*."FORMAT"

for TXT in ${file}
do
   IFS='.'
    set -- $TXT
    if ! grep $1 ../"REFERENCE FILE" > /dev/null
    then
	echo $1
	mv "$TXT" ../null
    fi
done
