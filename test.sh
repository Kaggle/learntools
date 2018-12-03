#!/bin/bash
#
# Run automated tests inside the latest Kaggle Python Docker base image.
set -e
set -x

echo "un: $KAGGLE_USERNAME"

docker run --rm -t \
    -v $PWD:/input:ro \
    gcr.io/kaggle-images/python:latest \
    /bin/bash -c '/input/notebooks/test.sh'
