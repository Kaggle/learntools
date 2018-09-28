#!/bin/bash

mkdir $1
mkdir $1/raw
mkdir $1/rendered
mkdir $1/kernels_api_metadata
cp track_meta_template.py $1/track_meta.py
touch $1/__init__.py
cp track_config_template.yaml $1/track_config.yaml

