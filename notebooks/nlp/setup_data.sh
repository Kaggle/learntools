#!/bin/bash
# Download the datasets used in the ML notebooks to correct relative_paths (../input/...)

set -e

if [ -d input ]
then
    exit 0
fi

mkdir -p input

DATASETS="matleonard/nlp-course alexisbcook/geospatial-learn-course-data"

for slug in $DATASETS
do
    name=`echo $slug | cut -d '/' -f 2`
    dest="input/$name"
    mkdir -p $dest
    kaggle d download -p $dest --unzip $slug
done

# COMPDATASETS="home-data-for-ml-course"

# for comp in $COMPDATASETS
# do 
#     dest="input/$comp"
#     mkdir -p $dest
#     kaggle competitions download $comp -p $dest
# done

# # the last exercise has only 1 dataset, so everything goes in input/ directly
# cp input/home-data-for-ml-course/* input

cd ..
