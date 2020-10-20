#!/bin/bash
set -ex

if [ -d input ]; then
    exit 0
fi
mkdir input

kaggle competitions download dog-breed-identification -p input/dog-breed-identification -f train.zip
unzip -q input/dog-breed-identification/train.zip -d input/dog-breed-identification/
rm input/dog-breed-identification/train.zip

kaggle datasets download keras/resnet50 -p input/resnet50
unzip -q input/resnet50/resnet50.zip -d input/resnet50/

kaggle datasets download -d keras/vgg16 -p input/vgg16
unzip -q input/vgg16/vgg16.zip -d input/vgg16/

kaggle datasets download dansbecker/hot-dog-not-hot-dog -p input/hot-dog-not-hot-dog/seefood --unzip

kaggle datasets download dansbecker/dogs-gone-sideways -p input/dogs-gone-sideways --unzip
mkdir input/dogs-gone-sideways/images
unzip -q input/dogs-gone-sideways/images.zip -d input/dogs-gone-sideways/images

kaggle datasets download zalando-research/fashionmnist -p input/fashionmnist --unzip

kaggle competitions download digit-recognizer -p input/digit-recognizer -f train.csv

kaggle datasets download -d dansbecker/urban-and-rural-photos -p input/urban-and-rural-photos --unzip
unzip -q input/urban-and-rural-photos/rural_and_urban_photos.zip -d input/urban-and-rural-photos/
rm -r input/urban-and-rural-photos/__MACOSX/
rm input/urban-and-rural-photos/*.zip

# Add utility script

SCRIPTS="ryanholbrook/petal-helper"

for script in $SCRIPTS
do
    name=`echo $script | cut -d '/' -f 2`
    dest="usr/lib"
    mkdir -p $dest
    kaggle kernels pull $script -p $dest
done
