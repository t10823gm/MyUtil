#!/bin/bash

##########
# duplicate yml file for array-job
#
# How to use
#    sh mkInputs.sh <inputs_dir> <data_dir>
#    (e.g.) sh mkInputs.sh inputs_1116 20171116_MCF10A
#########


SCRIPT_DIR=$(cd $(dirname $0); pwd)
#echo ${SCRIPT_DIR%/}/${1}

BASE_PATH="/home/gembu/CellTK/data"
DATA_DIR=${BASE_PATH%/}/${2}/'*'
#echo $DATA_DIR

rm ${SCRIPT_DIR%/}/${1%/}/*~ # remove backup file
template=$(ls ${SCRIPT_DIR%/}/${1})
echo $template
#template='input_MCF10A_Pos1.yml'

dirary=()
for filepath in $DATA_DIR; do
  if [ -d $filepath ] ; then
    dirary+=("$filepath")
  fi
done

# list of directory
for i in ${dirary[@]}; do
    pos=$(basename $i)
    templ=${SCRIPT_DIR%/}/${1%/}/${template}
    target=${SCRIPT_DIR%/}/${1%/}/${template/Pos1/$(basename $i)}
    echo $templ
    echo $target
    cp $templ $target
    sed -i -e "s/Pos1/$pos/g" $target
    #    cat $target | sed -e "s/Pos1/$pos/g"
done
