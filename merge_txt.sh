#!/bin/bash


max=`ls ./$1/$1*.txt | wc -l`

if [ $max -gt 9 ]; then
    format_string="%02d"
else
    format_string="%d"
fi

for i in $(seq 1 $max)
do
    findex=$(printf "$format_string" $i)
    cat ./$1/$1_${findex}.txt >> ./$1/${1}.txt
done




