#!/bin/bash

set -e

trackname() {
    echo $(dirname $1 | rev | cut -d '/' -f 1 | rev)
}

for nb in "$@"; do
    python3 clean.py $nb
    jupyter nbconvert --config partials/python/nbconvert_config.py \
       --to notebook \
       --output "$(basename $nb)" \
       --output-dir rendered/$(trackname $nb) \
      $nb
done
