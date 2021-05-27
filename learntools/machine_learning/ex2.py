import datetime
import pandas as pd

from learntools.core import *

class LoadHomeData(EqualityCheckProblem):
    _var = 'home_data'
    _hint = "Use the `pd.read_csv` function"
    _solution = CS('home_data = pd.read_csv(iowa_file_path)')

    def check(self, df):
        assert isinstance(df, pd.DataFrame), ("`home_data` should be a DataFrame,"
                " not `{}`").format(type(df),)
        expected_shape = (1460, 81)
        assert df.shape == expected_shape, ("Expected {} rows and {} columns, but"
                " got shape {}").format(expected_shape[0], expected_shape[1], df.shape)


class HomeDescription(EqualityCheckProblem):
    _vars = ['avg_lot_size', 'newest_home_age']
    max_year_built = 2010
    min_home_age = datetime.datetime.now().year - max_year_built
    _expected = [10517, min_home_age]
    _hint = 'Run the describe command. Lot size is in the column called LotArea. Also look at YearBuilt. Remember to round lot size '
    _solution = CS(
"""# using data read from home_data.describe()
avg_lot_size = 10517
newest_home_age = {}
""".format(min_home_age))


qvars = bind_exercises(globals(), [
    LoadHomeData,
    HomeDescription,
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
