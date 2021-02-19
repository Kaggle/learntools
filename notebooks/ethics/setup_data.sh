#!/bin/bash
set -ex

if [ -d input ]; then
    exit 0
fi
mkdir input

# Download the datasets used in the ML notebooks to correct relative_paths (../input/...)
DATASETS="alexisbcook/synthetic-credit-card-approval"

for slug in $DATASETS
do
    name=`echo $slug | cut -d '/' -f 2`
    dest="input/$name"
    mkdir -p $dest
    kaggle d download -p $dest --unzip $slug
done

COMPDATASETS="jigsaw-unintended-bias-in-toxicity-classification"

for comp in $COMPDATASETS
do
    dest="input/$comp"
    mkdir -p $dest
    kaggle competitions download $comp -p $dest
    cd $dest
    unzip ${comp}.zip
    chmod 700 *.csv
    cp *.csv ..
    cd ..
done
