#!/bin/bash

# Pasamos por parámetro el fichero con productos y el número de páginas
filename=$1
n_pages=$2 

while read line; do
# Leemos cada línea del fichero
echo "-----Término de búsqueda: $line"

python src/sailor.py "$line" $2
done < $filename