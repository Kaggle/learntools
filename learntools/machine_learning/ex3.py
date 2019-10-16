from numpy import array
import pandas as pd
import sklearn
from sklearn.tree import DecisionTreeRegressor

from learntools.core import *


class SetTarget(CodingProblem):
    _var = 'y'
    _hint = ("Use `print(home_data.columns)`. The column you want is at the end "
            "of the list. Use the dot notation to pull out this column from the DataFrame")
    _solution = CS('y = home_data.SalePrice')

    def check(self, targ):
        assert isinstance(targ, pd.Series), ("`home_data` should be a Pandas Series "
                                             "with the actual data. Your current "
                                             "answer is a `{}`").format(type(targ),)
        true_mean = 180921.19589041095
        assert int(targ.mean()) == int(true_mean), ("You've selected the wrong data.")


class SelectPredictionData(CodingProblem):
    _var = 'X'
    _hint = ("Capitalization and spelling are important when specifying variable names. "
             "Use the brackets notation when specifying data for X.")
    _solution = CS(
"""feature_names = ["LotArea", "YearBuilt", "1stFlrSF", "2ndFlrSF",
                      "FullBath", "BedroomAbvGr", "TotRmsAbvGrd"]

X=home_data[feature_names]""")
    def check(self, df):
        assert isinstance(df, pd.DataFrame), ("`X` should be a DataFrame,"
                " not `{}`").format(type(df),)
        expected_shape = (1460, 7)
        assert df.shape == expected_shape, ("Expected {} rows and {} columns, but"
                " got shape {}").format(expected_shape[0], expected_shape[1], df.shape)


class CreateModel(CodingProblem):
    _var = 'iowa_model'
    _hint = ("Include `random_state` when specifying model. Data is specified when fitting it.")
    _solution = CS("""from sklearn.tree import DecisionTreeRegressor
iowa_model = DecisionTreeRegressor(random_state=1)
iowa_model.fit(X, y)""")

    def check(self, dtree):
        # Not checking what they fit, because likely mistakes cause exceptions

        assert type(dtree) == type(DecisionTreeRegressor()), \
                    ("Expected `dtree` to be of type DecisionTreeRegressor but got an "
                     "object of type `{}`").format(type(dtree))
        assert dtree.random_state is not None, "You forgot to set the random_state."
        assert getattr(dtree, 'tree_', None) is not None, "You have not fit the model."



class MakePredictions(CodingProblem):
    _vars = ['predictions', 'iowa_model', 'X']
    _hint = """Use `iowa_model.predict` with an argument holding the data to predict with."""
    _solution = CS('iowa_model.predict(X)')
    def check(self, predictions, iowa_model, X):
        # This step is just checking that they can make predictions.
        # If we want to check model is correct, do it in fitting step.
        ground_truth = iowa_model.predict(X)
        assert ground_truth.shape[0] != 5, ("Your prediction results had 5 rows. They should have 1460. "
                                            "Did you call predict on the head() of the data rather than all of the data?")
        assert ground_truth.shape == predictions.shape, ("Your predictions are "
                    "shape {}. Expected shape {}").format(predictions.shape,  ground_truth.shape)
        assert all(predictions == ground_truth), ("Expected {} but got predictions {}").format(ground_truth, preds)


qvars = bind_exercises(globals(), [
    SetTarget,
    SelectPredictionData,
    CreateModel,
    MakePredictions
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
