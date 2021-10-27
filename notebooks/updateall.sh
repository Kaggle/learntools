#!/bin/bash

# Need to first update the macro 
# Then run this file.

set -e

# microchallenges (NOTE: does not update exercises)
python prepare_push.py microchallenges
kaggle k push -p microchallenges/prod/kernels_api_metadata/tut1
kaggle k push -p microchallenges/prod/kernels_api_metadata/tut2

# python (tut_3, ex_1 don't work)
python prepare_push.py python
kaggle k push -p python/prod/kernels_api_metadata/ex_2
kaggle k push -p python/prod/kernels_api_metadata/ex_3
kaggle k push -p python/prod/kernels_api_metadata/ex_4
kaggle k push -p python/prod/kernels_api_metadata/ex_5
kaggle k push -p python/prod/kernels_api_metadata/ex_6
kaggle k push -p python/prod/kernels_api_metadata/ex_7
kaggle k push -p python/prod/kernels_api_metadata/tut_1
kaggle k push -p python/prod/kernels_api_metadata/tut_2
kaggle k push -p python/prod/kernels_api_metadata/tut_4
kaggle k push -p python/prod/kernels_api_metadata/tut_5
kaggle k push -p python/prod/kernels_api_metadata/tut_6
kaggle k push -p python/prod/kernels_api_metadata/tut_7

# pandas (tut_0 doesn't work)
python prepare_push.py pandas
kaggle k push -p pandas/prod/kernels_api_metadata/ex_0
kaggle k push -p pandas/prod/kernels_api_metadata/ex_1
kaggle k push -p pandas/prod/kernels_api_metadata/ex_2
kaggle k push -p pandas/prod/kernels_api_metadata/ex_3
kaggle k push -p pandas/prod/kernels_api_metadata/ex_4
kaggle k push -p pandas/prod/kernels_api_metadata/ex_5
kaggle k push -p pandas/prod/kernels_api_metadata/tut_1
kaggle k push -p pandas/prod/kernels_api_metadata/tut_2
kaggle k push -p pandas/prod/kernels_api_metadata/tut_3
kaggle k push -p pandas/prod/kernels_api_metadata/tut_4
kaggle k push -p pandas/prod/kernels_api_metadata/tut_5

# intro to ML (need to edit link in final exercise back to tutorial)
python prepare_push.py machine_learning
./pushall.sh machine_learning/prod

# AI Ethics (ex3 and ex4 do not work)
python prepare_push.py ethics
kaggle k push -p ethics/prod/kernels_api_metadata/tut1
kaggle k push -p ethics/prod/kernels_api_metadata/tut2
kaggle k push -p ethics/prod/kernels_api_metadata/tut3
kaggle k push -p ethics/prod/kernels_api_metadata/tut4
kaggle k push -p ethics/prod/kernels_api_metadata/ex2

# intro to SQL
python prepare_push.py sql
./pushall.sh sql/prod

# ML explainability
python prepare_push.py ml_explainability
./pushall.sh ml_explainability/prod

# Data viz
python prepare_push.py data_viz_to_coder
./pushall.sh data_viz_to_coder/prod

# intermediate ML
python prepare_push.py ml_intermediate
./pushall.sh ml_intermediate/prod

# advanced SQL
python prepare_push.py sql_advanced
./pushall.sh sql_advanced/prod

# feature engineering
python prepare_push.py feature_engineering
./pushall.sh feature_engineering/prod

# geospatial analysis
python prepare_push.py geospatial
./pushall.sh geospatial/prod

# NLP
python prepare_push.py nlp
./pushall.sh nlp/prod

# game AI
python prepare_push.py game_ai
./pushall.sh game_ai/prod

# data cleaning
python prepare_push.py data_cleaning
./pushall.sh data_cleaning/prod

# intro to deep learning
python prepare_push.py deep_learning_intro
./pushall.sh deep_learning_intro/prod

# computer vision
python prepare_push.py computer_vision
./pushall.sh computer_vision/prod

