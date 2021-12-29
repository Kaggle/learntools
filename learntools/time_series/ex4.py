from learntools.core import *
from learntools.time_series.checking_utils import load_store_sales, load_family_sales
from learntools.time_series.utils import make_lags, make_leads


class Q1(EqualityCheckProblem):  # Plotting cycles
    family_sales = load_family_sales()
    y = family_sales.loc[:, ('sales', 'SCHOOL AND OFFICE SUPPLIES')].rename("Supply Sales")
    y_ma = y.rolling(7, center=True).mean()

    _vars = ['y_ma']
    _expected = [y_ma]

    _hint = """Your solution should look like:
```python
y_ma = y.rolling(____, center=____).____()

ax = y_ma.plot()
ax.set_title("Seven-Day Moving Average");
```
"""
    _solution = CS("""
y_ma = y.rolling(7, center=True).mean()

ax = y_ma.plot()
ax.set_title("Seven-Day Moving Average");
""")


class Q2(ThoughtExperiment):  # Serial dependence in Store Sales
    _solution = """The correlogram indicates the first lag is likely to be significant, as well as possibly the eighth lag. The lag plot suggests the effect is mostly linear.
"""


class Q3(ThoughtExperiment):  # Time series features
    _solution = """The lag plot indicates that both leading and lagged values of `onpromotion` are correlated with supply sales. This suggests that both kinds of values could be useful as features. There may be some non-linear effects as well.
"""


class Q4(EqualityCheckProblem):  # Create time series features
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    from statsmodels.tsa.deterministic import (CalendarFourier,
                                               DeterministicProcess)
    family_sales = load_family_sales()
    y = family_sales.loc[:, ('sales', 'SCHOOL AND OFFICE SUPPLIES')].rename("Supply Sales")
    onpromotion = family_sales.loc[:, ('onpromotion',
                                       'SCHOOL AND OFFICE SUPPLIES')].rename("onpromotion")
    fourier = CalendarFourier(freq='M', order=4)
    dp = DeterministicProcess(
        constant=True,
        index=y.index,
        order=1,
        seasonal=True,
        drop=True,
        additional_terms=[fourier],
    )
    X_time = dp.in_sample()
    X_time['NewYearsDay'] = (X_time.index.dayofyear == 1)
    model = LinearRegression(fit_intercept=False)
    model.fit(X_time, y)
    y_deseason = y - model.predict(X_time)
    y_deseason.name = 'sales_deseasoned'
    X_lags = make_lags(y_deseason, lags=1)
    X_promo = pd.concat([
        make_lags(onpromotion, lags=1),
        onpromotion,
        make_leads(onpromotion, leads=1),
    ],
                        axis=1)

    _vars = ['X_lags', 'X_promo']
    _expected = [X_lags, X_promo]

    _hint = """Your solution should look like:
```python
X_lags = make_lags(y_deseason, lags=____)

X_promo = pd.concat([
    make_lags(onpromotion, lags=____),
    onpromotion,
    make_leads(onpromotion, leads=____),
], axis=1)

X = pd.concat([X_time, X_lags, X_promo], axis=1).dropna()
y, X = y.align(X, join='inner')
```
"""
    _solution = CS("""
X_lags = make_lags(y_deseason, lags=1)

X_promo = pd.concat([
    make_lags(onpromotion, lags=1),
    onpromotion,
    make_leads(onpromotion, leads=1),
], axis=1)

X = pd.concat([X_time, X_lags, X_promo], axis=1).dropna()
y, X = y.align(X, join='inner')
""")


class Q5(EqualityCheckProblem):  # Create statistical features
    family_sales = load_family_sales()
    supply_sales = family_sales.loc(axis=1)[:, 'SCHOOL AND OFFICE SUPPLIES']
    y_lag = supply_sales.loc[:, 'sales'].shift(1)
    onpromo = supply_sales.loc[:, 'onpromotion']

    median_14 = y_lag.rolling(14).median()
    std_7 = y_lag.rolling(7).std()
    promo_7 = onpromo.rolling(7, center=True).sum()

    _vars = ['median_14', 'std_7', 'promo_7']
    _expected = [median_14, std_7, promo_7]

    _hint = """Your code should look like:
```python
y_lag = supply_sales.loc[:, 'sales'].shift(1)
onpromo = supply_sales.loc[:, 'onpromotion']

mean_7 = y_lag.rolling(7).____()
median_14 = y_lag.rolling(____).median()
std_7 = y_lag.rolling(____).____()
promo_7 = onpromo.rolling(____, center=True).____()
```
"""
    _solution = CS("""
y_lag = supply_sales.loc[:, 'sales'].shift(1)
onpromo = supply_sales.loc[:, 'onpromotion']

mean_7 = y_lag.rolling(7).mean()
median_14 = y_lag.rolling(14).median()
std_7 = y_lag.rolling(7).std()
promo_7 = onpromo.rolling(7, center=True).sum()
""")


qvars = bind_exercises(globals(), [Q1, Q2, Q3, Q4, Q5], var_format="q_{n}")
__all__ = list(qvars)
