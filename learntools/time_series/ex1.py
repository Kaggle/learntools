from learntools.core import *
from learntools.time_series.checking_utils import load_average_sales

average_sales = load_average_sales()


# Interpret linear regression with the time dummy
class Q1(ThoughtExperiment):
    _hint = ""
    _solution = ""


# Interpret linear regression with a lag feature
class Q2(ThoughtExperiment):
    _hint = ""
    _solution = ""


class Q3(EqualityCheckProblem):
    import numpy as np
    df = average_sales.to_frame()
    time = np.arange(len(df.index))
    df['time'] = time
    X = df.loc[:, ['time']]
    y = df.loc[:, 'sales']

    _vars = ['time', 'X', 'y']
    _expected = [time, X, y]
    _solution = CS("""
from sklearn.linear_model import LinearRegression

df = average_sales.to_frame()

time = np.arange(len(df.index))  # time dummy

df['time'] = time

X = df.loc[:, ['time']]  # features
y = df.loc[:, 'sales']  # target

model = LinearRegression()
model.fit(X, y)

y_pred = pd.Series(model.predict(X), index=X.index)
""")


class Q4(EqualityCheckProblem):
    import pandas as pd
    from sklearn.linear_model import LinearRegression

    df = average_sales.to_frame()
    lag_1 = df['sales'].shift(1)
    df['lag_1'] = lag_1
    X = df.loc[:, ['lag_1']]
    X.dropna(inplace=True)  # drop missing values in the feature set
    y = df.loc[:, 'sales']  # create the target
    y, X = y.align(X, join='inner')  # drop corresponding values in target

    model = LinearRegression()
    model.fit(X, y)

    y_pred = pd.Series(model.predict(X), index=X.index)

    _vars = ['lag_1', 'y_pred']
    _expected = [lag_1, y_pred]
    _solution = CS("""
df = average_sales.to_frame()

lag_1 = df['sales'].shift(1)

df['lag_1'] = lag_1

X = df.loc[:, ['lag_1']]
X.dropna(inplace=True)  # drop missing values in the feature set
y = df.loc[:, 'sales']  # create the target
y, X = y.align(X, join='inner')  # drop corresponding values in target

model = LinearRegression()
model.fit(X, y)

y_pred = pd.Series(model.predict(X), index=X.index)
""")


qvars = bind_exercises(globals(), [Q1, Q2, Q3, Q4], var_format="q_{n}")
__all__ = list(qvars)
