from learntools.core import *
from learntools.time_series.checking_utils import load_family_sales
from learntools.time_series.utils import make_lags, make_multistep_target


class Q1(EqualityCheckProblem):  # Match description to dataset
    _vars = ['task_a', 'task_b', 'task_c']
    _expected = [2, 1, 3]
    _hint = """The number of forecasting steps is the number of columns under **Targets**. The number of lags is the number of columns under **Features**. The lead time is the smallest lag step possible."""
    _solution = CS("""
task_a = 2
task_b = 1
task_c = 3
""")


class Q2(ThoughtExperiment):  # Forecasting task for Store Sales
    _solution = """The training set ends on `2017-08-15`, which gives us the forecast origin. The test set comprises the dates `2017-08-16` to `2017-08-31`, and this gives us the forecast horizon. There is one step between the origin and horizon, so we have a lead time of one day.

Put another way, we need a 16-step forecast with a 1-step lead time. We can use lags starting with lag 1, and we make the entire 16-step forecast using features from `2017-08-15`.
"""


class Q3(EqualityCheckProblem):  # Create multistep dataset for Store Sales
    family_sales = load_family_sales()
    y = family_sales.loc[:, 'sales']
    X = make_lags(y, lags=4).dropna()
    y = make_multistep_target(y, steps=16).dropna()
    y, X = y.align(X, join='inner', axis=0)

    _vars = ['X', 'y']
    _expected = [X, y]

    _hint = """Your solution should look like:
```python
y = family_sales.loc[:, 'sales']

X = make_lags(____, lags=____).dropna()

y = make_multistep_target(____, steps=____).dropna()

y, X = y.align(X, join='inner', axis=0)
```
"""
    _solution = CS("""
y = family_sales.loc[:, 'sales']

X = make_lags(y, lags=4).dropna()

y = make_multistep_target(y, steps=16).dropna()

y, X = y.align(X, join='inner', axis=0)
""")


class Q4(CodingProblem):  # Forecast with DirRec strategy
    _hint = """Your solution should look like:
```python
from sklearn.multioutput import RegressorChain

model = RegressorChain(base_estimator=____())
```
"""
    _solution = CS("""
from sklearn.multioutput import RegressorChain

model = RegressorChain(base_estimator=XGBRegressor())
""")
    _vars = ['model']

    def check(self, model):
        from sklearn.multioutput import RegressorChain
        from xgboost import XGBRegressor
        assert isinstance(
            model, RegressorChain
        ), f"Your model should be an instance of `RegressorChain`. It is actually a `{type(model)}`."
        assert not isinstance(
            model.base_estimator, type
        ), "You need to instantiate the base estimator, like `XGBRegressor()` instead of `XGBRegressor`."
        assert isinstance(
            model.base_estimator, XGBRegressor
        ), "The base estimator should be an instance of `XGBRegressor`. You provided `type(model.base_estimator)`."


qvars = bind_exercises(globals(), [Q1, Q2, Q3, Q4], var_format="q_{n}")
__all__ = list(qvars)
