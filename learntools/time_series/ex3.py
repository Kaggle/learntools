from learntools.core import *
from learntools.core.asserts import assert_equal
from learntools.time_series.checking_utils import load_average_sales


class Q1(ThoughtExperiment):  # Determine seasonality
    _hint = ""
    _solution = ""


class Q2(CodingProblem):  # Create seasonal features
    _vars = ['dp', 'X']

    def check(self, dp, X):
        from statsmodels.tsa.deterministic import (CalendarFourier,
                                                   DeterministicProcess)
        y = load_average_sales()['2017']
        fourier = CalendarFourier(freq='M', order=4)
        dp = DeterministicProcess(
            index=y.index,
            constant=True,
            order=1,
            seasonal=True,
            additional_terms=[fourier],
            drop=True,
        )
        X_true = dp.in_sample()

        import pandas as pd
        assert all(
            dp._index == y.index
        ), f"`index` argument to `DeterministicProcess` should be `y.index`. You gave {dp._index}."
        assert dp._constant, f"`constant` argument to `DeterministicProcess` should be `True`. You gave {dp._constant}."
        assert dp._order == 1, f"`order` argument to `DeterministicProcess` should be `1`. You gave {dp._order}."
        assert dp._seasonal, f"`seasonal` argument to `DeterministicProcess` should be `True`. You gave {dp._seasonal}."
        assert len(
            dp._additional_terms
        ) == 1, f"`additional_terms` argument to `DeterministicProcess` should be `[fourier]`. You gave {dp._additional_terms}."
        assert isinstance(
            dp._additional_terms[0], CalendarFourier
        ), f"`additional_terms` argument to `DeterministicProcess` should be `[fourier]`. You gave {dp._additional_terms}."
        assert dp._additional_terms[
            0]._order == 4, f"`order` argument to `CalendarFourier` should be `4`. You gave {dp._additional_terms[0]._order}."
        assert isinstance(
            dp._additional_terms[0]._freq, pd.offsets.MonthEnd
        ), f"`freq` argument to `CalendarFourier` should be `'M'`."
        assert dp._drop, f"`additional_terms` argument to `DeterministicProcess` should be `True`. You gave {dp._drop}."
        assert_equal(X, X_true, 'X')

    _hint = """Your answer should look like:
```python
y = average_sales.copy()

fourier = CalendarFourier(____)
dp = DeterministicProcess(
    index=y.index,
    constant=True,
    order=1,
    seasonal=____,
    additional_terms=[____],
    drop=True,
)
X = dp.in_sample()
```
"""
    _solution = CS("""
y = average_sales.copy()

fourier = CalendarFourier(freq='M', order=4)
dp = DeterministicProcess(
    index=y.index,
    constant=True,
    order=1,
    seasonal=True,
    additional_terms=[fourier],
    drop=True,
)
X = dp.in_sample()
""")


class Q3(ThoughtExperiment):  # Explore holiday events
    _hint = ""
    _solution = ""


class Q4(ThoughtExperiment):  # Check for remaining seasonality
    _hint = ""
    _solution = ""


qvars = bind_exercises(globals(), [Q1, Q2, Q3, Q4], var_format="q_{n}")
__all__ = list(qvars)
