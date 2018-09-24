#!/bin/bash

mkdir $1
mkdir $1/partials
mkdir $1/rendered
mkdir $1/pushables
cp track_meta_template.py $1/track_meta.py
touch $1/__init__.py
