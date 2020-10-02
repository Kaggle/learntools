#!/bin/bash

# Need to first update the macro 
# Then run this file.

set -e

# ex 7, ex automl
python prepare_push.py machine_learning
kaggle k push -p machine_learning/prod/kernels_api_metadata/ex7
kaggle k push -p machine_learning/prod/kernels_api_metadata/ex_automl

# ex1, ex2, ex3, ex4
python prepare_push.py ml_intermediate
kaggle k push -p ml_intermediate/prod/kernels_api_metadata/ex1
kaggle k push -p ml_intermediate/prod/kernels_api_metadata/ex2
kaggle k push -p ml_intermediate/prod/kernels_api_metadata/ex3
kaggle k push -p ml_intermediate/prod/kernels_api_metadata/ex4

# ex1, ex2, ex3, tut_halite
python prepare_push.py game_ai
kaggle k push -p game_ai/prod/kernels_api_metadata/ex1
kaggle k push -p game_ai/prod/kernels_api_metadata/ex2
kaggle k push -p game_ai/prod/kernels_api_metadata/ex3
kaggle k push -p game_ai/prod/kernels_api_metadata/tut_halite
