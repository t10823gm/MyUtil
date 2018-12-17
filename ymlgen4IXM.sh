#/bin/sh

#####
# sh ymlgen4IXM.sh "PATH2INPUTS" "PATH2IMGDIR"
####

BASE_PATH1="/home/gembu/CellTK/input_files"
SCRIPT_DIR=$(cd $(dirname $BASE_PATH1/$0); pwd)
#echo ${SCRIPT_DIR%/}/${1}

BASE_PATH2="/home/gembu/CellTK/data"
DATA_DIR=${BASE_PATH2%/}/${2}
#echo $DATA_DIR

rm ${SCRIPT_DIR%/}/${1%/}/*~ # remove backup file
template=$(ls ${SCRIPT_DIR%/}/${1})
fn=( `echo $template | tr -s '_' ' '`)
welldata=${fn[1]}
stagep=( `echo ${fn[-1]} | tr -s '.' ' '`)
#template='input_MCF10A_Pos1.yml'

find $DATA_DIR -type d | while read FILE
do
    #echo `find $FILE -type d | wc -l`
    if [ `find $FILE -type d | wc -l` -eq 1 ];then
	echo $FILE
	array=( `echo $FILE | tr -s '/' ' '`)
	newyml=input_${array[-2]}_${array[-1]}.yml
	templ=${SCRIPT_DIR%/}/${1%/}/${template}
	target=${SCRIPT_DIR%/}/${1%/}/${newyml}
	echo ${templ}
	echo ${target}
	cp $templ $target
	sed -i -e "s/$welldata/${array[-2]}/g" $target
	sed -i -e "s/$stagep/${array[-1]}/g" $target
    fi
done
