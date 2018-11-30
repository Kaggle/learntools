#!/bin/bash
#
# Run automated testing for our notebooks.
set -e
set -x

# Testing whether initial pwd is writable
touch test.txt

# path to the notebook/ directory.
DIR=`dirname "${BASH_SOURCE[0]}"`
cd $DIR
TMP_DIR=`mktemp -d`

# Install packages the notebook pipeline depends on but which aren't installed with the learntools package.
pip3 install -r requirements.txt

TRACKS="embeddings pandas python"
for track in $TRACKS
do
    # Run each step of the rendering pipeline, to make sure it runs without errors.
    # TODO: These fail because the install is in a read-only FS. Should either add
    # a --dry-run flag to these, or allow specifying a custom output directory.
    #python3 clean.py $track
    #python3 prepare_push.py $track
    #python3 render.py $track
    echo "pass"
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
