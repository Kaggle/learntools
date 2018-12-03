#!/bin/bash
#
# Run automated testing for our notebooks.
set -e
set -x

# path to the notebook/ directory.
DIR=`dirname "${BASH_SOURCE[0]}"`
# Install learntools branch
pip3 install $DIR/..
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
    # TODO: Fails due to failure when calling get_git_branch()
    #python3 render.py $track
done

TESTABLE_NOTEBOOK_TRACKS="python pandas"
for track in $TESTABLE_NOTEBOOK_TRACKS
do
    cd $track
    ! [[ -a setup_data.sh ]] || ./setup_data.sh
    for nb in `ls raw/*.ipynb`
    do
        # Skip some known bugs/misbehaving tests
        if ((
            # First pandas reference notebook has a bug (b/120286668), and times out.
            [[ $nb =~ "writing-reference" ]]
            # First python exercise notebook uses google/tinyquickdraw dataset, which
            # is 11 GB. Downloading it would probably slow down testing unacceptably.
            || ( [[ $nb =~ "ex_1" ]] && [[ $track == "python" ]] )
            ))
        then
            echo "Warning: skipping $nb in track $track"
            continue
        fi
        jupyter nbconvert --output-dir "$TMP_DIR" --execute $nb
    done
    cd ../
done
