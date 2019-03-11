import pandas as pd
import warnings

from learntools.core import *

class GetScore(CodingProblem):
    _vars = ['X_train_1', 'X_valid_1']
    _hint = ("Use `pd.get_dummies()`, and ensure the columns are in the same order in both datasets "
        "with the `align()` method. This is just one potential solution - try out other methods by "
        "referencing the tutorial on categorical variables!")
    _solution = CS(
"""# one-hot encode categorical data
X_train_1 = pd.get_dummies(X_train)
X_valid_1 = pd.get_dummies(X_valid)

# ensure columns are in same order in both datasets
X_train_1, X_valid_1 = X_train_1.align(X_valid_1, join='inner', axis=1)
""")
    
    def check(self, X_train_1, X_valid_1):

        assert not(any((X_train_1.dtypes == 'object').values)), \
        "It looks like your dataset still contains categorical columns that need to be preprocessed."

        assert len(X_train_1.columns) == len(X_valid_1.columns), \
        ("Please ensure your training and validation data have the same number of columns. For this, "
            "you can use the `align()` method.")

        assert all(X_train_1.columns == X_valid_1.columns), \
        ("Please ensure your training and validation data have the same column ordering. "
            "For this, you can use the `align()` method.")

class GetDict(CodingProblem):
    _vars = ['X_train_2', 'X_valid_2']
    _hint = ("Use `SimpleImputer()`. This is just one potential solution - try out other methods by "
        "referencing the tutorial on missing values!")
    _solution = CS(
"""# make copy to avoid changing original data (when imputing)
""")
    
    def check(self, results):

        # columns with missing values
        assert type(results) == dict, \
        "`results` does not appear to be a Python dictionary."
        
        assert len(results) == 8, \
        "`results` should have 8 entries, one for each tested value of `n_estimators`."
        
        assert list(results.keys()) == [50*i for i in range(1,9)], \
        ("The keys in `results` do not appear to be correct.  Please ensure you have one key for each "
         "tested value of `n_estimators`.")

class BestScore(CodingProblem):
    _var = 'score'
    _hint = ("Find the key corresponding to the minimum value in the `results` dictionary "
             "from the previous step.  This will tell you which value for `n_estimators` "
             "gets the lowest average MAE.")
    _solution = CS("n_estimators_best = min(results, key=results.get)")
    
    def check(self, score):
        assert score != 100, \
        ("You should find the value for `n_estimators` with the minimum score, not the maximum score.")
        
        assert score < 18000, \
        ("It looks like you have provided an average MAE value.  Please instead provide a value for "
         "`n_estimators` that indicates the ideal number of trees to use in the model.")
        
        assert score == 200, \
        ("Find the key corresponding to the minimum value in the `results` dictionary.")
    
qvars = bind_exercises(globals(), [
    GetScore,
    GetDict,
    BestScore
    ],
    tutorial_id=-1,
    var_format='step_{n}',
    )
__all__ = list(qvars)
