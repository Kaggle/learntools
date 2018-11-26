#!/bin/bash

# Call me passing in a track directory as a command line argument, and I'll push all the notebooks in that track.

set -e

# NB: Depending on whether $1 ends in a /, you might get //, and it turns out that's totally okay. That's convenient.
for subdir in $(find $1/kernels_api_metadata -mindepth 1 -maxdepth 1 -type d); do
    kaggle k push -p $subdir
done
