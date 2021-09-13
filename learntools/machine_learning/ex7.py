import numpy as np
from numpy import array
import pandas as pd
from learntools.core import *

class CheckSubmittablePreds(CodingProblem):
    _var = 'test_preds'
    _solution = CS("""
# In previous code cell
rf_model_on_full_data = RandomForestRegressor()
rf_model_on_full_data.fit(X, y)

# Then in last code cell
test_data_path = '../input/test.csv'
test_data = pd.read_csv(test_data_path)
test_X = test_data[features]
test_preds = rf_model_on_full_data.predict(test_X)


output = pd.DataFrame({'Id': test_data.Id,
                       'SalePrice': test_preds})
output.to_csv('submission.csv', index=False)
""")

    def check(self, test_preds):
        assert type(test_preds) == np.ndarray, "test_preds should be a numpy array but instead it is {}".format(type(test_preds))
        assert test_preds.shape == (1459,), "Your predictions don't look right. It should be a numpy array of shape (1459,). But the actual shape is {}".format(test_preds.shape)

qvars = bind_exercises(globals(), [
    CheckSubmittablePreds
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
