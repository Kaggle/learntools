import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from learntools.core import *

class BestModel(CodingProblem):
    _var = 'best_model'
    _hint = ("Which model gets the lowest MAE score?")
    _solution = CS(
"""best_model = model_3
""")
    
    def check(self, best_model):

        assert type(best_model) == RandomForestRegressor, \
        ("Set the value of `best_model` to one of `model_1`, `model_2`, " 
         "`model_3`, `model_4`, or `model_5`.") 
        
        params = best_model.get_params()
        assert params['n_estimators'] == 100 and params['criterion'] == 'mae' \
        and params['random_state'] == 0, \
        ("Set the value of `best_model` to one of `model_1`, `model_2`, " 
         "`model_3`, `model_4`, or `model_5`.  Select the model that gets the lowest MAE.") 

class Predictions(CodingProblem):
    _var = 'my_model'
    _hint = ("You need only set `my_model` to a random forest model.  The rest of the code "
             "is written for you!")
    _solution = CS(
"""# Define a model
my_model = best_model

try: 
    # Fit the model on the training and validation data
    my_model.fit(X, y)
    # Generate test predictions
    preds_test = my_model.predict(X_test)
    # Save predictions in format used for competition scoring
    output = pd.DataFrame({'Id': X_test.index,
                       'SalePrice': preds_test})
    output.to_csv('submission.csv', index=False)
except AttributeError:
    pass
""")
    
    def check(self, my_model):
        assert 'sklearn' in str(type(my_model)), \
        "The model defined in `my_model` does not appear to be a valid scikit-learn model!"
        
        df = pd.read_csv('./submission.csv')
        assert os.path.isfile('./submission.csv') and list(df.columns) == ['Id', 'SalePrice'] \
        and len(df) == 1459, \
        ("It looks like you edited the provided code that creates the submission file.  Please "
         "convert it back to the original.")

qvars = bind_exercises(globals(), [
    BestModel,
    Predictions,
    ],
    tutorial_id=-1,
    var_format='step_{n}',
    )
__all__ = list(qvars)
