#!/bin/bash
set -ex

if [ -d input ]; then
    exit 0
fi
mkdir input

# Download the datasets used in the ML notebooks to correct relative_paths (../input/...)
DATASETS=("alexisbcook/synthetic-credit-card-approval" "alexisbcook/jigsaw-snapshot")

for dataset in "${DATASETS[@]}"
do
    name=`echo $dataset | cut -d '/' -f 2`
    dest="input/$name"
    mkdir -p $dest
    kaggle d download -p $dest --unzip $dataset
done