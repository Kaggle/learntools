#!/bin/bash
#
# Run automated testing for our notebooks.
set -e
set -x

# path to the notebook/ directory.
DIR=`dirname "${BASH_SOURCE[0]}"`
# The learntools repo is cloned to a read-only location. Various testing steps involve writing,
# so copy the whole notebooks directory to a writeable location and work from there.
WORKING_DIR=`mktemp -d`
cp -r $DIR $WORKING_DIR
cd $WORKING_DIR/notebooks

TMP_DIR=`mktemp -d`

# Install packages the notebook pipeline depends on but which aren't installed with the learntools package.
pip3 install -r requirements.txt

TRACKS="embeddings pandas python"
for track in $TRACKS
do
    # Run each step of the rendering pipeline, to make sure it runs without errors.
    python3 clean.py $track
    python3 prepare_push.py $track
    python3 render.py $track
done

# For now, just run one notebook (which doesn't depend on any datasets)
jupyter nbconvert --output-dir "$TMP_DIR" --execute "python/raw/ex_2.ipynb"

TESTABLE_NOTEBOOK_TRACKS="pandas"
for track in $TESTABLE_NOTEBOOK_TRACKS
do
    cd $track
    ./setup_data.sh
    for nb in `ls raw/*.ipynb`
    do
        # XXX: First pandas reference notebook has a bug (b/120286668), and times out.
        if [[ $nb =~ "writing-reference" ]]
        then
            continue
        fi
        jupyter nbconvert --output-dir "$TMP_DIR" --execute $nb
    done
done
