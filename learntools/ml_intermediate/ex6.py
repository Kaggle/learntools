import pandas as pd
import xgboost
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

from learntools.core import *

# Load the data
X = pd.read_csv('../input/train.csv', index_col='Id')
X_test_full = pd.read_csv('../input/test.csv', index_col='Id')
X.dropna(axis=0, subset=['SalePrice'], inplace=True)
y = X.SalePrice
X.drop(['SalePrice'], axis=1, inplace=True)
X_train_full, X_valid_full, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2,
                                                                random_state=0)
low_cardinality_cols = [cname for cname in X_train_full.columns if X_train_full[cname].nunique() < 10 and
                        X_train_full[cname].dtype == "object"]
numeric_cols = [cname for cname in X_train_full.columns if X_train_full[cname].dtype in ['int64', 'float64']]
my_cols = low_cardinality_cols + numeric_cols
X_train = X_train_full[my_cols].copy()
X_valid = X_valid_full[my_cols].copy()
X_test = X_test_full[my_cols].copy()
X_train = pd.get_dummies(X_train)
X_valid = pd.get_dummies(X_valid)
X_test = pd.get_dummies(X_test)
X_train, X_valid = X_train.align(X_valid, join='left', axis=1)
X_train, X_test = X_train.align(X_test, join='left', axis=1)

# Define and train basic model
basic_model = XGBRegressor(random_state=0)
basic_model.fit(X_train, y_train)
basic_predictions = basic_model.predict(X_valid)
basic_mae = mean_absolute_error(basic_predictions, y_valid)

class Model1A(CodingProblem):
    _var = 'my_model_1'
    _hint = ("Begin by defining the model with `my_model_1 = XGBRegressor(random_state=0)`. "
             "Then, you can fit the model with the `fit()` method.")
    _solution = CS(
"""# Define the model
my_model_1 = XGBRegressor(random_state=0)

# Fit the model
my_model_1.fit(X_train, y_train)
""")

    def check(self, my_model_1):
        assert type(my_model_1) == xgboost.sklearn.XGBRegressor, \
        "Please make `my_model_1` an instance of the `XGBRegressor` class in the `xgboost` package."

        assert my_model_1.get_params() == basic_model.get_params(), \
        ("Please instantiate the XGBoost model with default parameters, and set the random seed "
         "to 0 (e.g., `my_model_1 = XGBRegressor(random_state=0)`).")

        try: 
            my_model_1.get_booster()
        except:
            assert 0==1, "Please fit the model to the training data."

class Model1B(CodingProblem):
    _var = 'predictions_1'
    _hint = ("Use the `predict()` method to generate validation predictions.")
    _solution = CS(
"""# Get predictions
predictions_1 = my_model_1.predict(X_valid)
""")

    def check(self, predictions_1):
        assert len(predictions_1) != 1168, \
        "Please generate predictions on the validation data, not the training data."

        assert len(predictions_1) == 292, \
        "Please generate predictions on the validation data."

        assert round(predictions_1[0]) == round(basic_predictions[0]), \
        ("Are you sure that you used the training data to train the model?"
         "Your validation predictions seem incorrect.")

class Model1C(CodingProblem):
    _var = 'mae_1'
    _hint = ("The `mean_absolute_error` function should take the predictions in `predictions_1` "
             "and the validation target in `y_valid` as arguments.")
    _solution = CS(
"""# Calculate MAE
mae_1 = mean_absolute_error(predictions_1, y_valid)
print("Mean Absolute Error:" , mae_1)
""")

    def check(self, mae_1):
        assert round(mae_1) == round(basic_mae), \
        "The value that you've calculated for the MAE is incorrect."

Model1 = MultipartProblem(Model1A, Model1B, Model1C)

class Model2(CodingProblem):
    _vars = ['my_model_2', 'predictions_2', 'mae_2']
    _hint = ("In the official solution to this problem, we chose to increase the number of trees in the model "
             "(with the `n_estimators` parameter) and decrease the learning rate (with the `learning_rate` parameter).")
    _solution = CS(
"""# Define the model
my_model_2 = XGBRegressor(n_estimators=1000, learning_rate=0.05)

# Fit the model
my_model_2.fit(X_train, y_train)

# Get predictions
predictions_2 = my_model_2.predict(X_valid)

# Calculate MAE
mae_2 = mean_absolute_error(predictions_2, y_valid)
print("Mean Absolute Error:" , mae_2)
""")

    def check(self, my_model_2, predictions_2, mae_2):
        assert type(my_model_2) == xgboost.sklearn.XGBRegressor, \
        "Please make `my_model_2` an instance of the `XGBRegressor` class in the `xgboost` package."

        assert len(predictions_2) != 1168, \
        "Please generate predictions on the validation data, not the training data."

        assert len(predictions_2) == 292, \
        "Please generate predictions on the validation data."

        assert round(mae_2) < round(basic_mae), \
        ("You must specify the parameters in `my_model_2` so that it attains lower MAE than the "
         "model in `my_model_1`.")

class Model3(CodingProblem):
    _vars = ['my_model_3', 'predictions_3', 'mae_3']
    _hint = ("In the official solution for this problem, we chose to greatly decrease the number of trees "
             "in the model by tinkering with the `n_estimators` parameter.")
    _solution = CS(
"""# Define the model
my_model_3 = XGBRegressor(n_estimators=1)

# Fit the model
my_model_3.fit(X_train, y_train)

# Get predictions
predictions_3 = my_model_3.predict(X_valid)

# Calculate MAE
mae_3 = mean_absolute_error(predictions_3, y_valid)
print("Mean Absolute Error:" , mae_3)
""")

    def check(self, my_model_3, predictions_3, mae_3):
        assert type(my_model_3) == xgboost.sklearn.XGBRegressor, \
        "Please make `my_model_3` an instance of the `XGBRegressor` class in the `xgboost` package."

        assert len(predictions_3) != 1168, \
        "Please generate predictions on the validation data, not the training data."

        assert len(predictions_3) == 292, \
        "Please generate predictions on the validation data."

        assert round(mae_3) > round(basic_mae), \
        ("You must specify the parameters in `my_model_3` so that it attains higher MAE than the "
         "model in `my_model_1`.")

qvars = bind_exercises(globals(), [
    Model1,
    Model2,
    Model3
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
