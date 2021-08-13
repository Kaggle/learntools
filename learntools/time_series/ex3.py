from learntools.core import *
from learntools.core.asserts import assert_equal
from learntools.time_series.checking_utils import load_average_sales, load_holidays_events


class Q1(ThoughtExperiment):  # Determine seasonality
    _solution = """Both the seasonal plot and the periodogram suggest a strong weekly seasonality. From the periodogram, it appears there may be some monthly and biweekly components as well. In fact, the notes to the *Store Sales* dataset say wages in the public sector are paid out biweekly, on the 15th and last day of the month -- a possible origin for these seasons.
"""


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


class Q3(ThoughtExperiment):  # Check for remaining seasonality
    _solution = """The periodogram for the deseasonalized series lacks any large values. By comparing it to the periodogram for the original series, we can see that our model was able to capture the seasonal variation in *Average Sales*.
"""


class Q4(EqualityCheckProblem):  # Create holiday features
    import pandas as pd

    holidays_events = load_holidays_events()
    # National and regional holidays in the training set
    holidays = (  #
        holidays_events  #
        .query("locale in ['National', 'Regional']")  #
        .loc['2017':'2017-08-15', ['description']]  #
        .assign(
            description=lambda x: x.description.cat.remove_unused_categories()
        )  #
    )  #

    X_holidays = pd.get_dummies(holidays).to_numpy()

    _vars = ['X_holidays']
    _expected = [X_holidays]

    _hints = [
        """With Pandas, you could use `pd.get_dummies`. With scikit-learn, you could use `sklearn.preprocessing.OneHotEncoder`. Using Pandas makes it easier to join `X_holidays` to `X2` since it returns a `DataFrame` retaining the date of each holiday.""",
        """In Pandas, your solution would look like:

```python
X_holidays = pd.get_dummies(____)

X2 = X.join(X_holidays, on='date').fillna(0.0)
```
<p>
In scikit-learn, your solution would look like:

```python
from sklearn.preprocessing import OneHotEncoder

ohe = OneHotEncoder(sparse=False)

X_holidays = pd.DataFrame(
    ____,
    index=____,
    columns=holidays.description.unique(),  # optional,  but nice to have
)

X2 = X.join(X_holidays, on='date').fillna(0.0)
```
"""
    ]
    _solution = CS("""
# Scikit-learn solution
from sklearn.preprocessing import OneHotEncoder

ohe = OneHotEncoder(sparse=False)

X_holidays = pd.DataFrame(
    ohe.fit_transform(holidays),
    index=holidays.index,
    columns=holidays.description.unique(),
)


# Pandas solution
X_holidays = pd.get_dummies(holidays)


# Join to training data
X2 = X.join(X_holidays, on='date').fillna(0.0)
""")


qvars = bind_exercises(globals(), [Q1, Q2, Q3, Q4], var_format="q_{n}")
__all__ = list(qvars)
