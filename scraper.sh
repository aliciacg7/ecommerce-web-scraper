#!/bin/bash
filename='data/product_list.txt'
n_pages=$1 

while read line; do
# reading each line
echo "-----Término de búsqueda: $line"

python src/sailor.py "$line" $1
done < $filename