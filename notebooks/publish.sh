#!/bin/bash

set -e

for nb in "$@"; do
    jupyter nbconvert --config partials/python/nbconvert_config.py \
       --to notebook \
       --output "$(basename $nb)" \
      --output-dir rendered \
      $nb
done
