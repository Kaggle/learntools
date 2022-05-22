import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from learntools.core import *

class BestModel(CodingProblem):
    _var = 'best_model'
    _hint = ("Which model gets the lowest MAE score?")
    _solution = CS(
"""best_model = model_3
""")

    def check(self, best_model):

        assert type(best_model) == RandomForestRegressor, \
        ("Set the value of `best_model` to one of `model_1`, `model_2`, "
         "`model_3`, `model_4`, or `model_5`.")

        params = best_model.get_params()
        assert params['n_estimators'] == 100 and (params['criterion'] == 'mae' or params['criterion'] == 'absolute_error') \
        and params['random_state'] == 0, \
        ("Set the value of `best_model` to one of `model_1`, `model_2`, "
         "`model_3`, `model_4`, or `model_5`.  Select the model that gets the lowest MAE.")

class Predictions(CodingProblem):
    _var = 'my_model'
    _hint = ("You need only set `my_model` to a random forest model.  You are welcome (but "
             "not required) to choose one of the five models above.")
    _solution = CS(
"""# Define a model
my_model = best_model
""")

    def check(self, my_model):
        assert type(my_model) == RandomForestRegressor, \
        "Please change `my_model` to a random forest model."

qvars = bind_exercises(globals(), [
    BestModel,
    Predictions,
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
