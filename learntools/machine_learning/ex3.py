from numpy import array
import pandas as pd
import sklearn
from learntools.core.utils import bind_exercises
from learntools.core.problem_factories import simple_problem
from learntools.core.richtext import CodeSolution as CS
from learntools.core.problem import *


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

class ChoosePredictors(EqualityCheckProblem):
    _var = 'predictor_names'
    _expected = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF',
                 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']
    _hint = ("Create a list of strings with the specified names. Capitalization "
             "and spelling is important.")
    _solution = CS(
"""predictor_names = ["LotArea", "YearBuilt", "1stFlrSF", "2ndFlrSF",
                      "FullBath", "BedroomAbvGr", "TotRmsAbvGrd"]
    """)

class SelectPredictionData(CodingProblem):
    _var = 'X'
    _hint = 'Set X equal to home data with the right set of predictors. Use the brackets notation.'
    _solution = CS(
"""# requires you have set predictor_names correctly
X=home_data[predictor_names]""")
    def check(self, df):
        assert isinstance(df, pd.DataFrame), ("`X` should be a DataFrame,"
                " not `{}`").format(type(df),)
        expected_shape = (1460, 7)
        assert df.shape == expected_shape, ("Expected {} rows and {} columns, but"
                " got shape {}").format(expected_shape[0], expected_shape[1], df.shape)


class SpecifyModel(CodingProblem):
    _var = 'iowa_model'
    _hint = ("You will need to import DecisionTreeRegressorModel but you want need "
             "to supply arguments when calling it.")
    _solution = CS("""from sklearn.tree import DecisionTreeRegressor
iowa_model = DecisionTreeRegressor(random_state=1)""")

    def check(self, dtree):
        assert type(dtree) == sklearn.tree.tree.DecisionTreeRegressor, \
                    ("Expected type object of type DecisionTreeRegressor but got an "
                     "object of type {}").format(type(dtree))
        assert dtree.random_state == 1

class FitModel(CodingProblem):
    _var = 'iowa_model'
    _hint = 'The only arguments you need for the fit method have been stored as X and y'
    _solution = CS("""iowa_model.fit(X, y)""")
    def check(self, iowa_model):
        # most mistakes in fitting will cause Exceptions. Accept anything for now
        pass

class MakePredictions(CodingProblem):
    _vars = ['first_preds', 'iowa_model', 'X']
    _hint = """Use iowa_model.predict with an argument holding the data to predict with.
    Use head on the predictors rather than the predictions."""
    _solution = 'iowa_model.predict(X.head())'
    def check(self, preds):
        ground_truth = iowa_model.predict(X.head())
        preds_len = len(preds)
        assert (preds_len == 5), ("Expected 5 predictions. Received {}. Did you use head()?").format(preds_len)
        assert all(preds == ground_truth), ("Expected {} but got predictions {}").format(ground_truth, preds)


qvars = bind_exercises(globals(), [
    SetTarget,
    ChoosePredictors,
    SelectPredictionData,
    SpecifyModel,
    FitModel,
    MakePredictions
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
