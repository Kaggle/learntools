#!/bin/bash
#
# Run automated testing for our notebooks.
set -e

# Print the commit hash and build date of the image the tests are running in.
if [[ -r /etc/git_commit ]]; then
    GIT_COMMIT=`cat /etc/git_commit`
    BUILD_DATE=`cat /etc/build_date`
    echo "Running inside image built at $BUILD_DATE for commit $GIT_COMMIT"
fi

# Filter by tracks if first argument set.
TRACKS="ml_explainability intro_to_programming time_series ethics feature_engineering_new computer_vision deep_learning_intro pandas python machine_learning sql data_viz_to_coder ml_intermediate sql_advanced feature_engineering geospatial nlp game_ai data_cleaning"
TESTABLE_NOTEBOOK_TRACKS="ml_intermediate ml_explainability intro_to_programming geospatial time_series ethics feature_engineering_new data_viz_to_coder data_cleaning computer_vision deep_learning_intro python pandas machine_learning game_ai"

if [[ -n $1 && $1 != "all" ]]; then
    TRACKS=$1
    TESTABLE_NOTEBOOK_TRACKS=$1
fi
readonly TRACKS
readonly TESTABLE_NOTEBOOK_TRACKS

# Filter by notebook if second argument set.
NOTEBOOK_FILTER=".*"
if [[ -n $2 && $2 != "all" ]]; then
    NOTEBOOK_FILTER=$2
fi
readonly NOTEBOOK_FILTER

echo "TRACKS='$TRACKS'"
echo "TESTABLE_NOTEBOOK_TRACKS='$TESTABLE_NOTEBOOK_TRACKS'"
echo "NOTEBOOK_FILTER='$NOTEBOOK_FILTER'"

# path to the notebook/ directory.
DIR=`dirname "${BASH_SOURCE[0]}"`
# Path to the parent (learntools) dir
LT=$(readlink -f $DIR/..)
# The learntools repo is cloned to a read-only location. Various testing steps involve writing,
# so copy the whole notebooks directory to a writeable location and work from there.
WORKING_DIR=`mktemp -d`
cp -r $LT $WORKING_DIR

# source retry.sh functions script.
source $DIR/retry.sh

# Install learntools branch
pip install $WORKING_DIR/input

cd $WORKING_DIR/input/notebooks

TMP_DIR=`mktemp -d`

# Install packages the notebook pipeline depends on but which aren't installed with the learntools package.
pip install -q -r requirements.txt

for track in $TRACKS
do
    # Run each step of the rendering pipeline, to make sure it runs without errors.
    python3 prepare_push.py $track
done

setup_data() {
    if [[ -a setup_data.sh ]]; then
        rm -rf input/ # delete input/ to start from a clean slate after a retry.
        ./setup_data.sh
    else
        echo "no setup_data.sh file. Skipping..."
    fi
}

for track in $TESTABLE_NOTEBOOK_TRACKS
do
    # Running the deep learning notebooks is fairly slow (~10-20 minutes), so only
    # do it if any of the relevant files have changed between this branch and master.
    #if [[ $track == "deep_learning" ]] && git diff --exit-code master -- $track ../learntools/$track; then
    #    echo "No changes affecting deep learning track. Skipping running notebooks."
    #    continue
    #fi
    cd $track
    with_retry 3 10 2 setup_data
    for nb in `ls raw/*.ipynb`
    do
        if [[ ! $nb =~ $NOTEBOOK_FILTER ]]; then
            # Skiping notebook because it doesn't match the notebook filter.
            continue
        fi
        # First python exercise notebook uses google/tinyquickdraw dataset, which
        # is 11 GB. Downloading it would probably slow down testing unacceptably.
        # AutoML notebooks also run for hours.
        if [[ ( $nb =~ "ex_1" && $track == "python" ) ]] \
            || [[ ( $nb =~ "ex_automl") ]] || [[ ( $nb =~ "tut_automl") ]] \
            || [[ ( $nb =~ "tut4" && $track == "game_ai" ) ]] \
            || [[ ( $nb =~ "tut4" && $track == "data_cleaning" ) ]] \
            || [[ ( $nb =~ "tut1" && $track == "intro_to_programming" ) ]] \
	    || [[ ( $nb =~ "tut2" && $track == "intro_to_programming" ) ]] \
	    || [[ ( $nb =~ "tut3" && $track == "intro_to_programming" ) ]] \
	    || [[ ( $nb =~ "ex8" && $track == "machine_learning" ) ]] \
            || [[ $nb =~ "tut_tpus" ]] || [[ $nb =~ "ex_tpus" ]] \
            || [[ ( $nb =~ "tut1" && $track == "computer_vision" ) ]] || [[ ( $nb =~ "tut5" && $track == "computer_vision" ) ]] || [[ ( $nb =~ "tut6" && $track == "computer_vision" ) ]] \
            || [[ ( $nb =~ "ex1" && $track == "computer_vision" ) ]] || [[ ( $nb =~ "ex5" && $track == "computer_vision" ) ]] || [[ ( $nb =~ "ex6" && $track == "computer_vision" ) ]] \
            || [[ ( $nb =~ "ex1" && $track == "computer_vision" ) ]] \
            || [[ ( $nb =~ "ex2" && $track == "nlp" ) ]] \
            || [[ ( $nb =~ "ex3_partial_plots" && $track == "ml_explainability" ) ]]
        then
            echo "Warning: skipping $nb in track $track"
            continue
        fi
        echo "Running nbconvert for $nb in track $track"
        jupyter nbconvert --output-dir "$TMP_DIR" --execute $nb --ExecutePreprocessor.timeout=1000 --to html
    done
    cd ../
done
