#!/bin/bash

set -o allexport
source .env
set +o allexport

if  [ ! -d "$1" ]; then
    mkdir $1
fi

if [ ! -f $1.mp3 ]; then
    ffmpeg -i $1.mp4 -q:a 0 -map a $1.mp3
fi

mp3splt $1.mp3 -t 15.0 -d ./$1  -a -o @f_@n

max=`ls ./$1/$1*.mp3 | wc -l`

if [ $max -gt 9 ]; then
    format_string="%02d"
else
    format_string="%d"
fi

for i in $(seq 1 $max)
do
    findex=$(printf "$format_string" $i)
    ffmpeg -i ./$1/$1_${findex}.mp3 ./$1/$1_${findex}.wav
done


for i in $(seq 1 $max)
do
    findex=$(printf "$format_string" $i)
    whisperx ./$1/$1_${findex}.wav -o ./$1/ --model=large --diarize --language=Polish --hf_token=$HF_TOKEN  --compute_type=float32 --output_format=all
done


python3 ./merge.py $1

tokens_file="tokens.txt"

vtt=./$1/$1.vtt

cp $vtt ${vtt}.bak

while IFS= read -r line; do
    line=$(echo "$line" | xargs)
    # Jeśli linia nie jest pusta
    if [ -n "$line" ]; then
        # Rozdzielenie tokena i zamiennika przy pomocy separatora =>
        token=$(echo "$line" | awk -F'=>' '{print $1}' | xargs)
        replacement=$(echo "$line" | awk -F'=>' '{print $2}' | xargs)
        # Zamiana w pliku VTT
        sed -i "s/$token/$replacement/g" "$vtt"
    fi
    echo $token
    echo $replacement
    sed -i "s/$token/$replacement/g" "$vtt"
done < "$tokens_file"


echo "Zamiany tokenów zostały wykonane w pliku: $vtt"





