import pandas as pd

from learntools.core.utils import bind_exercises
from learntools.core.problem_factories import simple_problem
from learntools.core.richtext import CodeSolution as CS
from learntools.core.problem import *


class SetTarget(VarCreationProblem):
    _var = 'y'
    _hint = "Use `print(home_data.columns)`. The column you want is at the end of the list. Use the dot notation to pull out this column from the DataFrame"
    _solution = CS('y = home_data.SalePrice')

    def check(self, targ):
        assert isinstance(targ, pd.Series), ("`home_data` should be a Pandas Series with the actual data. Your current answer is a"
                "  `{}`").format(type(targ),)
        true_mean = 180921.19589041095
        assert int(targ.mean()) == int(true_mean), ("You've selected the wrong data.")

class ChoosePredictors(VarCreationProblem):
    _vars = ['predictor_names']
    _expected = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']
    _hint = 'Create a list of strings with the specified names. Capitalization and spelling is important.'
    _solution = CS(
"""predictor_names = ["LotArea", "YearBuilt", "1stFlrSF", "2ndFlrSF", "FullBath", "BedroomAbvGr", "TotRmsAbvGrd"]
    """)

class SelectPredictionData(VarCreationProblem):
    _vars = ['X']
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

class SpecifyModel(VarCreationProblem):
    _vars = ['iowa_model']
    _hint = ['You will need to import DecisionTreeRegressorModel but you want need to supply arguments when calling it.]
    def check(self, dtree):
        from sklearn.tree import DecisionTreeRegressor
        assert type(dtree) = sklearn.tree.tree.DecisionTreeRegressor, ("Expected type object of type DecisionTreeRegressor but got an object of type {}").format(type(dtree))

class FitModel():

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
