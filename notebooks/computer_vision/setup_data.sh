#!/bin/bash


set -e

if [ -d input ]
then
    exit 0
fi

# Setup Datsets
mkdir -p input

DATASETS=("ryanholbrook/stanford-cars-for-learn" "ryanholbrook/cv-course-models" "ryanholbrook/computer-vision-resources")

for dataset in "${DATASETS[@]}"
do
    name=`echo $dataset | cut -d '/' -f 2`
    dest="input/$name"
    mkdir -p $dest
    kaggle d download -p $dest --unzip $dataset
done


# Setup Utility Scripts
SCRIPTS=("ryanholbrook/visiontools" "ryanholbrook/cv-prelude")

for script in "${SCRIPTS[@]}"
do
    name=`echo $script | cut -d '/' -f 2`
    dest="usr/lib"
    mkdir -p $dest
    kaggle kernels pull $script -p $dest
done

echo "Contents of usr/lib"
ls usr/lib
