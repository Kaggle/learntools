from learntools.core import *
from learntools.time_series.ex5setup import *


class Q1(CodingProblem):  # Fit method for boosted hybrid
    def check(self, BoostedHybrid):
        from sklearn.utils.validation import check_is_fitted

        # imported from ex5setup
        bh = BoostedHybrid(LinearRegression(), KNeighborsRegressor())

        X_1, X_2 = X, X.stack().to_frame()

        try:
            bh.fit(X_1, X_2, y)
        except Exception as e:
            if 'Placeholder' in e.args[0]:
                raise exceptions.NotAttempted
            else:
                raise e

        try:
            check_is_fitted(bh.model_1,
                            msg='Fit not implemented correctly for `model_1`.')
        except:
            assert False

        try:
            check_is_fitted(bh.model_2,
                            msg='Fit not implemented correctly for `model_2`.')
        except:
            assert False

        assert bhe.y_fit.equals(bh.y_fit), \
            'Fit not implemented correctly for `model_1`.'

        assert bhe.y_resid.equals(bh.y_resid), \
            'Residual series y_resid not implemented correctly.'

        assert all(bhe.model_2.predict(X_2) == bh.model_2.predict(X_2)), \
            'Fit not implemented correctly for `model_2`.'

    _vars = ["BoostedHybrid"]

    _hint = """Your solution should look like:
```python
def fit(self, X_1, X_2, y):
    # Fit self.model_1
    self.model_1.fit(X_1, y)

    # Make predictions with self.model_1
    y_fit = pd.DataFrame(
        self.model_1.____(____), 
        index=X_1.index, columns=y.columns,
    )

    # Compute residuals
    y_resid = y - ____
    y_resid = y_resid.stack().squeeze() # wide to long

    # Train model_2 on residuals
    self.model_2.fit(____, ____)

    # Save column names for predict method
    self.y_columns = y.columns
    # Save data for question checking
    self.y_fit = y_fit
    self.y_resid = y_resid


# Add method to class
BoostedHybrid.fit = fit
```
"""
    _solution = CS("""
def fit(self, X_1, X_2, y):
    # Train model_1
    self.model_1.fit(X_1, y)

    # Make predictions
    y_fit = pd.DataFrame(
        self.model_1.predict(X_1), 
        index=X_1.index, columns=y.columns,
    )

    # Compute residuals
    y_resid = y - y_fit
    y_resid = y_resid.stack().squeeze() # wide to long

    # Train model_2 on residuals
    self.model_2.fit(X_2, y_resid)

    # Save column names for predict method
    self.y_columns = y.columns
    # Save data for question checking
    self.y_fit = y_fit
    self.y_resid = y_resid


# Add method to class
BoostedHybrid.fit = fit
""")


class Q2(CodingProblem):  # Predict method for boosted hybrid
    def check(self, BoostedHybrid):
        from sklearn.utils.validation import check_is_fitted

        # imported from ex5setup
        bh = BoostedHybrid(LinearRegression(), KNeighborsRegressor())
        X_1, X_2 = X, X.stack().to_frame()

        try:
            bh.fit(X_1, X_2, y)
        except:
            assert False, "Implement `fit` method correctly first."

        try:
            bh.predict(X_1, X_2)
        except Exception as e:
            if 'Placeholder' in e.args[0]:
                raise exceptions.NotAttempted
            else:
                raise e

        assert bhe.predict(X_1, X_2).equals(bh.predict(X_1, X_2))

    _vars = ["BoostedHybrid"]
    _hint = """Your solution should look like:
```python
def predict(self, X_1, X_2):
    # Predict with model_1
    y_pred = pd.DataFrame(
        self.model_1.____(____), 
        index=X_1.index, columns=self.y_columns,
    )
    y_pred = y_pred.stack().squeeze()  # wide to long

    # Add model_2 predictions to model_1 predictions
    y_pred += self.model_2.____(____)

    return y_pred.unstack()


# Add method to class
BoostedHybrid.predict = predict
```
"""
    _solution = CS("""
def predict(self, X_1, X_2):
    # Predict with model_1
    y_pred = pd.DataFrame(
        self.model_1.predict(X_1), 
        index=X_1.index, columns=self.y_columns,
    )
    y_pred = y_pred.stack().squeeze()  # wide to long

    # Add model_2 predictions to model_1 predictions
    y_pred += self.model_2.predict(X_2)

    return y_pred.unstack()


# Add method to class
BoostedHybrid.predict = predict
""")


class Q3(CodingProblem):  # Train boosted hybrid
    def check(self, model):
        from xgboost import XGBRegressor

        assert isinstance(
            model.model_1, LinearRegression
        ), "model_1 should be an instance of LinearRegression."
        assert isinstance(
            model.model_2,
            XGBRegressor), "model_2 should be an instance of XGBRegressor."

    _vars = ['model']

    _hint = """Your solution should look like:
```python
# Create model
model = BoostedHybrid(
    model_1=____,
    model_2=____,
)
model.fit(X_1, X_2, ____)

y_pred = model.predict(____, ____)
y_pred = y_pred.clip(0.0)
```
"""
    _solution = CS("""
# Create model
model = BoostedHybrid(
    model_1=LinearRegression(),
    model_2=XGBRegressor(),
)
model.fit(X_1, X_2, y)

y_pred = model.predict(X_1, X_2)
y_pred = y_pred.clip(0.0)
""")


class Q4(ThoughtExperiment):  # Fit with different learning algorithms
    _hint = ""
    _solution = ""


qvars = bind_exercises(globals(), [Q1, Q2, Q3, Q4], var_format="q_{n}")
__all__ = list(qvars)
