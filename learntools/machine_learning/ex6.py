import numpy as np
from numpy import array
import pandas as pd
import sklearn
from sklearn.tree import DecisionTreeRegressor
from learntools.core import *

class CheckRfScore(CodingProblem):
    _var = 'rf_val_mae'
    _hint = 'Review the code above with a DecisionTreeRegressor. Use the RandomForestRegressor instead'
    _solution = CS("""rf_model = RandomForestRegressor()

# fit your model
rf_model.fit(train_X, train_y)

# Calculate the mean absolute error of your Random Forest model on the validation data
rf_val_predictions = rf_model.predict(val_X)
rf_val_mae = mean_absolute_error(rf_val_predictions, val_y)
""")

    def check(self, rf_val_mae):
        assert type(rf_val_mae) in [float, np.float64], "Expected rf_val_mae to be a number with a decimal type. Observed type {}".format(type(rf_val_mae))
        # rf_val_mae should be 22,883. Giving wiggle room to handle version differences, etc.
        assert rf_val_mae > 20000, "Your validation score of {} is implausibly low.".format(rf_val_mae)
        assert rf_val_mae < 25000, "Your validation score of {} is higher than it should be.".format(rf_val_mae)

qvars = bind_exercises(globals(), [
    CheckRfScore
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
