#!/bin/bash
# Download the datasets used in the ML notebooks to correct relative_paths (../input/...)

mkdir -p input

DATASETS="ryanholbrook/fe-course-data"

for slug in $DATASETS
do
    name=`echo $slug | cut -d '/' -f 2`
    dest="input/$name"
    mkdir -p $dest
    kaggle d download -p $dest --unzip $slug
done


COMPDATASETS="house-prices-advanced-regression-techniques"

for comp in $COMPDATASETS
do 
    dest="input/$comp"
    mkdir -p $dest
    kaggle competitions download $comp -p $dest
    cd $dest
    unzip ${comp}.zip
    chmod 700 *.csv
    cp *.csv ..
    cd ../..
done

