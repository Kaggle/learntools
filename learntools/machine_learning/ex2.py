import pandas as pd

from learntools.core.utils import bind_exercises
from learntools.core.richtext import CodeSolution as CS
from learntools.core.problem import *

class LoadHomeData(VarCreationProblem):
    _var = 'home_data'
    _hint = "Use the `pd.read_csv` function"
    _solution = CS('home_data = pd.read_csv(iowa_file_path)')

    def check(self, df):
        assert isinstance(df, pd.DataFrame), ("`home_data` should be a DataFrame,"
                " not `{}`").format(type(df),)
        expected_shape = (1460, 81)
        assert df.shape == expected_shape, ("Expected {} rows and {} columns, but"
                " got shape {}").format(expected_shape[0], expected_shape[1], df.shape)

class HomeDescription(VarCreationProblem):
    _vars = ['ave_lot_size', 'newest_home_age']
    _expected = [10517, 8]
    _hint = 'Run the describe command. Lot size is another name for Lot Area'
    _solution = 'idk'

# Shorter syntax equivalent to above
from learntools.core.problem_factories import simple_problem
hd = simple_problem('HomeDescription', solution='idk', hint='This is a hint')\
        .with_expected(avg_lot_size=10516.828, newest_home_age=8)

qvars = bind_exercises(globals(), [
    LoadHomeData,
    HomeDescription,
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
