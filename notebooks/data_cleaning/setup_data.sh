#!/bin/bash
set -ex

if [ -d input ]; then
    exit 0
fi
mkdir input

DATASETS="maxhorowitz/nflplaybyplay2009to2016 aparnashastry/building-permit-applications-data kemical/kickstarter-projects nasa/landslide-events usgs/earthquake-database smithsonian/volcanic-eruptions kwullum/fatal-police-shootings-in-the-us alexisbcook/pakistan-intellectual-capital"

for slug in $DATASETS
do
    name=`echo $slug | cut -d '/' -f 2`
    dest="input/$name"
    mkdir -p $dest
    kaggle d download -p $dest --unzip $slug
done