#!/bin/bash

set -e

if [ -d input ]
then
    exit 0
fi

mkdir -p input

DATASETS="maxhorowitz/nflplaybyplay2009to2016 aparnashastry/building-permit-applications-data aaronschlegel/seattle-pet-licenses kemical/kickstarter-projects kwullum/fatal-police-shootings-in-the-us zusmani/pakistansuicideattacks"

for slug in $DATASETS
do
    name=`echo $slug | cut -d '/' -f 2`
    dest="input/$name"
    mkdir -p $dest
    kaggle d download -p $dest --unzip $slug
done