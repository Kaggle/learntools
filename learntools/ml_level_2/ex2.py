import pandas as pd
import warnings

from learntools.core import *

class DealCats(CodingProblem):
    _vars = ['X_train_1', 'X_valid_1']
    _hint = ("Use `pd.get_dummies()`, and ensure the columns are in the same order in both datasets "
        "with the `align()` method. This is just one potential solution - try out other methods by "
        "referencing the tutorial on categorical variables!")
    _solution = CS(
"""# One-hot encode categorical data
X_train_1 = pd.get_dummies(X_train)
X_valid_1 = pd.get_dummies(X_valid)

# Ensure columns are in same order in both datasets
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

class DealMiss(CodingProblem):
    _vars = ['X_train_2', 'X_valid_2']
    _hint = ("Use `SimpleImputer()`. This is just one potential solution - try out other methods by "
             "referencing the tutorial on missing values!")
    _solution = CS(
"""# Make copy to avoid changing original data (when imputing)
X_train_imp = X_train_1.copy()
X_valid_imp = X_valid_1.copy()

# Get names of columns with missing values
cols_with_missing = [col for col in X_train_1.columns if X_train_1[col].isnull().any()]

# Make new columns indicating what will be imputed
for col in cols_with_missing:
    X_train_imp[col + '_was_missing'] = X_train_1[col].isnull()
    X_valid_imp[col + '_was_missing'] = X_valid_1[col].isnull()
    
# Imputation
my_imputer = SimpleImputer()
X_train_2 = pd.DataFrame(my_imputer.fit_transform(X_train_imp))
X_valid_2 = pd.DataFrame(my_imputer.transform(X_valid_imp))

# Imputation removed column names; put them back
X_train_2.columns = X_train_imp.columns
X_valid_2.columns = X_valid_imp.columns
""")
    
    def check(self, X_train_2, X_valid_2):

        # columns with missing values
        X_2 = pd.concat([X_train_2, X_valid_2])
        cols_with_missing = [col for col in X_2.columns if X_2[col].isnull().any()]
        
        assert len(cols_with_missing) == 0, \
        "It looks like your dataset still contains columns with missing data."

class Score(CodingProblem):
    _var = 'score'
    _hint = ("Run the code cell without any changes to get your MAE score, which must be "
             "less than 18000.  If you do not pass, check out the hints in Step 1 and Step 2 "
             "to learn one way to preprocess your data.")
    _solution = ""
    
    def check(self, score):

        assert score < 18000, \
        ("Check out the hints in Step 1 and Step 2 to learn one way that you can preprocess your data.")
    
qvars = bind_exercises(globals(), [
    DealCats,
    DealMiss,
    Score
    ],
    tutorial_id=-1,
    var_format='step_{n}',
    )
__all__ = list(qvars)
