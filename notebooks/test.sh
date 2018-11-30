#!/bin/bash
#
# Run automated testing for our notebooks.
set -e
set -x

# path to the notebook/ directory.
DIR=`dirname "${BASH_SOURCE[0]}"`
TMP_DIR=`mktemp -d`

# Install packages the notebook pipeline depends on but which aren't installed with the learntools package.
pip3 install -r "$DIR/requirements.txt"

# TRACKS="embeddings pandas python"
# for track in $TRACKS
# do
#     # Run each step of the rendering pipeline, to make sure it runs without errors.
#     python3 clean.py $track
#     python3 prepare_push.py $track
#     python3 render.py $track

#     # TODO: Once basic checks are working we should also do the following here:
#     # - download necessary datasets for this track
#     # - nbconvert execute *all* exercise notebooks for the track
# done

# For now, just run one notebook (which doesn't depend on any datasets)
jupyter nbconvert --output "$TMP_DIR" --execute "$DIR/python/raw/ex_2.ipynb"
