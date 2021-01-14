#!/bin/bash
#
# Run automated tests inside the staging Kaggle Python Docker base image.
set -e
set -x

docker run --rm -t \
    -e KAGGLE_USERNAME -e KAGGLE_KEY \
    -v $PWD:/input:ro \
    gcr.io/kaggle-images/python:staging \
    /bin/bash -c '/input/notebooks/test.sh'
