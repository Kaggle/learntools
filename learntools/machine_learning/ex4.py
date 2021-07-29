from numpy import array
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from learntools.core import *

class SplitData(CodingProblem):
    # test are on train_X and val_y. If these are right, others will be right too.
    _vars = ["train_X", "val_X", "train_y", "val_y", "X", "y"]
    _hint = ("The function you need to import is part of sklearn. When calling "
             "the function, the arguments are X and y. Ensure you set the random_state to 1.")
    _solution = CS("""from sklearn.model_selection import train_test_split
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)""")

    def check(self, train_X, val_X, train_y, val_y, X, y):

        true_train_X, _, _, true_val_y = \
                    [i for i in train_test_split(X, y, random_state=1)]
        assert train_X.shape == true_train_X.shape, ("Expected `train_X` to have shape {}. "
                                                     "Your code produced `train_X` with shape {}."
                                                     ).format(true_train_X.shape, train_X.shape)
        assert val_y.shape == true_val_y.shape, ("Expected `val_y` to have shape {}. "
                                                     "Your code produced `val_y` with shape {}."
                                                     ).format(true_val_y.shape, val_y.shape)
        # Verify they have set the seed correctly, to help with later steps
        assert all(train_X.index == true_train_X.index), "The training data had different rows than expected"


class FitModelWithTrain(CodingProblem):
    _vars = ['iowa_model', 'train_X', 'train_y', 'val_X']
    _hint = 'Remember, you fit with training data. You will test with validation data soon'
    _solution = CS("""iowa_model = DecisionTreeRegressor(random_state=1)
iowa_model.fit(train_X, train_y)""")

    def check(self, iowa_model, train_X, train_y, val_X):
        assert iowa_model.tree_, "You have not fit your model yet."
        assert iowa_model.random_state == 1, "Ensure you created your model with `random_state=1`"
        # Fitting this model is cheap. So we do it in check
        correct_model = DecisionTreeRegressor(random_state=1)
        correct_model.fit(train_X, train_y)
        expected_pred = correct_model.predict(val_X.head(10))
        actual_pred = iowa_model.predict(val_X.head(10))
        print(expected_pred)
        print(actual_pred)
        assert all(actual_pred == expected_pred), (
                    "Model was tested by predicting the value of first row training data. "
                    "Expected prediction of `{}`. Model actually predicted `{}`. "
                    "Did you set the `random_state` and pass the right data?").format(expected_pred, actual_pred)

class ValPreds(CodingProblem):
    _vars = ['val_predictions', 'iowa_model', 'val_X']
    _hint = 'Run predict on the right validation data object.'
    _solution = CS("""val_predictions = iowa_model.predict(val_X)""")

    def check(self, val_predictions, iowa_model, val_X):
        assert val_predictions.size == 365, "`val_predictions` is wrong size. Did you predict with the correct data? The dataset `val_X` contains the validation observations."
        comparison_val_preds = iowa_model.predict(val_X)
        assert all(comparison_val_preds == val_predictions), ("Predictions do not match expectations. "
                                                             "Did you supply the right data? The dataset `val_X` contains the validation observations.")

class MAE(EqualityCheckProblem):
    _var = 'val_mae'
    _expected = 29652.931506849316
    _hint = ("The order of arguments to mean_absolute_error doesn't matter. Make sure you fit to only the training data in step 2.")
    _solution = CS("""val_mae = mean_absolute_error(val_y, val_predictions)""")


qvars = bind_exercises(globals(), [
    SplitData,
    FitModelWithTrain,
    ValPreds,
    MAE
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
