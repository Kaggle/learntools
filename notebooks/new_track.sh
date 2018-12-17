#!/bin/bash

mkdir $1
mkdir $1/raw
cp nb_utils/track_meta_template.py $1/track_meta.py
touch $1/__init__.py
cp nb_utils/track_config_template.yaml $1/default.yaml

