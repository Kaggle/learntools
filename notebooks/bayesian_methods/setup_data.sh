#!/bin/bash
set -e

mkdir -p input

DATASETS="dansbecker/training-sky dansbecker/bayesian-methods"

for slug in $DATASETS
do
    name=`echo $slug | cut -d '/' -f 2`
    dest="input/$name"
    mkdir -p $dest
    kaggle d download -p $dest --unzip $slug
done

cd ..
