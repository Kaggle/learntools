#!/bin/bash
set -ex

if [ -d input ]; then
    exit 0
fi
mkdir input

DATASETS=("ryanholbrook/car-or-truck" "ryanholbrook/cv-course-models" "ryanholbrook/computer-vision-resources")

for dataset in "${DATASETS[@]}"
do
    name=`echo $dataset | cut -d '/' -f 2`
    dest="input/$name"
    mkdir -p $dest
    kaggle d download -p $dest --unzip $dataset
done
