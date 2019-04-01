import pandas as pd
import xgboost
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

from learntools.core import *
    
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
        
        default_params = {'base_score': 0.5, 'booster': 'gbtree', 'colsample_bylevel': 1,
                          'colsample_bytree': 1, 'gamma': 0, 'learning_rate': 0.1, 'max_delta_step': 0,
                          'max_depth': 3, 'min_child_weight': 1, 'missing': None, 'n_estimators': 100,
                          'n_jobs': 1, 'nthread': None, 'objective': 'reg:linear', 'random_state': 0,
                          'reg_alpha': 0, 'reg_lambda': 1, 'scale_pos_weight': 1, 'seed': None,
                          'silent': True, 'subsample': 1}
        assert my_model_1.get_params() == default_params, \
        ("Please instantiate the XGBoost model with default parameters, and set the random seed "
         "to 0 (e.g., `my_model_1 = XGBRegressor(random_state=0)`).")
        
        assert my_model_1._Booster is not None, \
        "Please fit the model to the training data."
        
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
        
        assert round(predictions_1[0]) == 237696, \
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
        assert round(mae_1) == 16803, \
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
        
        assert round(mae_2) < 16803, \
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
        
        assert round(mae_3) > 16803, \
        ("You must specify the parameters in `my_model_3` so that it attains higher MAE than the "
         "model in `my_model_1`.")

qvars = bind_exercises(globals(), [
    Model1,
    Model2,
    Model3
    ],
    tutorial_id=-1,
    var_format='step_{n}',
    )
__all__ = list(qvars)
