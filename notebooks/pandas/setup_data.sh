#!/bin/bash
# Download the datasets used in the Pandas notebooks and move them around such that they're available to the notebooks
# at relative paths (../input/...) that mimic where files would be available in kernels.

set -e

if [ -d input ]
then
    exit 0
fi

mkdir -p input

# NB: In many cases, notebooks only use one or two files from the dataset. Possible
# we could save some time/bandwidth using the -f argument to kaggle d download.
DATASETS="zynicide/wine-reviews nolanbconaway/pitchfork-data open-powerlifting/powerlifting-database residentmario/things-on-reddit jpmiller/publicassistance datasnaek/youtube-new"

for slug in $DATASETS
do
    name=`echo $slug | cut -d '/' -f 2`
    dest="input/$name"
    mkdir -p $dest
    kaggle d download -p $dest --unzip $slug
done

# Things on reddit is a zip of a zip. Kaggle d --unzip doesn't do a deep unzip, but kernels does
unzip -q input/things-on-reddit/top-things.zip -d input/things-on-reddit/top-things

# Setup a shallow symlink for the wine reviews dataset. Some ref notebooks only
# have the one dataset attached.
cd input
ln -s wine-reviews/winemag-data-130k-v2.csv .
cd ..
