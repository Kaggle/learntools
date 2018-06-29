from numpy import array
import pandas as pd
import sklearn
from learntools.core.utils import bind_exercises
from learntools.core.problem_factories import simple_problem
from learntools.core.richtext import CodeSolution as CS
from learntools.core.problem import *


class SplitData(CodingProblem):
    _vars = [train_X, val_X, train_y, val_y]
    _hint = ("The function you need to import is part of sklearn. When calling "
             "the function, the arguments are X and y")
    _solution = CS("""from sklearn.model_selection import train_test_split
train_x, val_X, train_y, val_y = train_test_split(X, y)""")

    def check(self, train_X, val_X, train_y, val_y):
        true_train_X_shape, true_val_X_shape, true_train_y_shape, true_val_y_shape =
                                        (1095, 7), (365, 7), (1095,) (365,)
        assert train_X.shape == true_train_X_shape, ("Expected train_X to have shape {}. "
                                                     "Your code produced train_X with shape {}."
                                                     ).format(true_train_X_shape, train_X.shape)
        assert val_X.shape == true_val_X_shape, ("Expected val_X to have shape {}. "
                                                     "Your code produced val_X with shape {}."
                                                     ).format(true_val_X_shape, val_X.shape)
        assert train_y.shape == true_train_y_shape, ("Expected train_y to have shape {}. "
                                                     "Your code produced train_y with shape {}."
                                                     ).format(true_train_y_shape, train_y.shape)
        assert val_y.shape == true_val_y_shape, ("Expected val_y to have shape {}. "
                                                     "Your code produced val_y with shape {}."
                                                     ).format(true_val_y_shape, val_y.shape)
        # Verify they have set the seed correctly, to ensure
        train_X.iloc[0,0] == 10084
        val_X.iloc[100,2] == 1168

#TODO: Fit Model, Make Predictions on Val Data, Calculate MAE steps

qvars = bind_exercises(globals(), [
    SplitData,
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
