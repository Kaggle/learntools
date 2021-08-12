from learntools.core import *
from learntools.time_series.checking_utils import (load_average_sales,
                                                   load_retail_sales)


class Q1(EqualityCheckProblem):  # Determine trend with MA plot
    food_sales = load_retail_sales().loc[:, 'FoodAndBeverage']
    trend = food_sales.rolling(
        window=12,
        center=True,
        min_periods=6,
    ).mean()

    _vars = ['trend']
    _expected = [trend]
    _hint = """Your answer should look like:
```python
trend = food_sales.rolling(
    window=____,
    center=____,
    min_periods=6,
).____()
```
"""
    _solution = CS("""
trend = food_sales.rolling(
    window=12,
    center=True,
    min_periods=6,
).mean()
""")


class Q2(ThoughtExperiment):  # Identify trend
    _solution = """The upwards bend in the trend suggests an order 2 (quadratic) polynomial might be appropriate.

If you've worked with economic time series before, you might guess that the growth rate in *Food and Beverage Sales* is best expressed as a percent change. Percent change can often be modeled using an exponential curve. (Don't worry if this isn't familiar!)
"""


class Q3(EqualityCheckProblem):  # Create trend feature
    from statsmodels.tsa.deterministic import DeterministicProcess

    y = load_average_sales()
    dp = DeterministicProcess(index=y.index, order=3)
    X = dp.in_sample()
    X_fore = dp.out_of_sample(steps=90)

    _vars = ['X', 'X_fore']
    _expected = [X, X_fore]
    _hint = """Your answer should look like:
```python
from statsmodels.tsa.deterministic import DeterministicProcess

y = average_sales.copy()

dp = DeterministicProcess(index=____, order=____)
X = dp.in_sample()
X_fore = dp.out_of_sample(steps=____)
```
"""
    _solution = CS("""
from statsmodels.tsa.deterministic import DeterministicProcess

y = average_sales.copy()

dp = DeterministicProcess(index=y.index, order=3)
X = dp.in_sample()
X_fore = dp.out_of_sample(steps=90)
""")


class Q4(ThoughtExperiment):  # Risks of high-order polynomials
    _hint = """What could you say about the rate of change of a term like `t ** 11` over a long period of time?"""
    _solution = """An order 11 polynomial will include terms like `t ** 11`. Terms like these tend to diverge rapidly outside of the training period making forecasts very unreliable."""


qvars = bind_exercises(globals(), [Q1, Q2, Q3, Q4], var_format="q_{n}")
__all__ = list(qvars)
