#!/bin/bash


set -e

if [ -d input ]
then
    exit 0
fi


# Add utility script

SCRIPTS="ryanholbrook/visiontools"

for script in $SCRIPTS
do
    name=`echo $script | cut -d '/' -f 2`
    dest="usr/lib"
    mkdir -p $dest
    kaggle kernels pull $script -p $dest
done
