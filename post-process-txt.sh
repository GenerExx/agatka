#!/bin/bash


tokens_file="tokens.txt"

vtt=./$1/$1.txt

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
#    echo $token
#    echo $replacement
    sed -i "s/$token/$replacement/g" "$vtt"
done < "$tokens_file"


echo "Zamiany tokenów zostały wykonane w pliku: $vtt"





