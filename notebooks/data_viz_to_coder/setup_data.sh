#!/bin/bash
set -ex

if [ -d input ]; then
    exit 0
fi
mkdir input

kaggle datasets download alexisbcook/data-for-datavis -p input
unzip -q input/data-for-datavis.zip -d input
chmod 644 input/*.csv
