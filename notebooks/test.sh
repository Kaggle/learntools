#!/bin/bash
#
# Run automated testing for our notebooks.
set -e
set -x

# path to the notebook/ directory.
DIR=`dirname "${BASH_SOURCE[0]}"`
# Path to the parent (learntools) dir
LT=$(readlink -f $DIR/..)
# Install learntools branch
pip3 install $DIR/..
# The learntools repo is cloned to a read-only location. Various testing steps involve writing,
# so copy the whole notebooks directory to a writeable location and work from there.
WORKING_DIR=`mktemp -d`
cp -r $LT $WORKING_DIR
cd $WORKING_DIR/input/notebooks

TMP_DIR=`mktemp -d`

# Install packages the notebook pipeline depends on but which aren't installed with the learntools package.
pip3 install -r requirements.txt

TRACKS="deep_learning embeddings pandas python machine_learning"
for track in $TRACKS
do
    # Run each step of the rendering pipeline, to make sure it runs without errors.
    python3 clean.py $track
    # If this fails (i.e. if running clean.py results in changes to the working tree),
    # this means that clean.py wasn't run before committing.
    git diff --exit-code $track
    python3 prepare_push.py $track
    # TODO: Fails due to failure when calling get_git_branch()
    #python3 render.py $track
done

TESTABLE_NOTEBOOK_TRACKS="deep_learning python pandas machine_learning"
for track in $TESTABLE_NOTEBOOK_TRACKS
do
    cd $track
    ! [[ -a setup_data.sh ]] || ./setup_data.sh
    for nb in `ls raw/*.ipynb`
    do
        # Skip some known bugs/misbehaving tests
        # First pandas reference notebook has a bug (b/120286668), and times out.
        # First python exercise notebook uses google/tinyquickdraw dataset, which
        # is 11 GB. Downloading it would probably slow down testing unacceptably.
        if [[ $nb =~ "writing-reference" || ( $nb =~ "ex_1" && $track == "python" ) ]]
        then
            echo "Warning: skipping $nb in track $track"
            continue
        fi
        jupyter nbconvert --output-dir "$TMP_DIR" --execute $nb --ExecutePreprocessor.timeout=1000
    done
    cd ../
done
