import pandas as pd
import warnings

from learntools.core import *

class Drop(CodingProblem):
    _vars = ['drop_X_train', 'drop_X_valid']
    _hint = ("Use the [`select_dtypes()`](https://pandas.pydata.org/pandas-"
             "docs/stable/reference/api/pandas.DataFrame.select_dtypes.html) method "
             "to drop all columns with the `object` dtype.")
    _solution = CS(
"""# Drop columns in training and validation data
drop_X_train = X_train.select_dtypes(exclude=['object'])
drop_X_valid = X_valid.select_dtypes(exclude=['object'])
""")
    
    def check(self, drop_X_train, drop_X_valid):
        
        assert type(drop_X_train) == pd.core.frame.DataFrame, \
        "`drop_X_train` is not a pandas DataFrame."
        
        assert type(drop_X_valid) == pd.core.frame.DataFrame, \
        "`drop_X_valid` is not a pandas DataFrame."

        assert not(any((drop_X_train.dtypes == 'object').values)), \
        "You still need to encode some of the categorical columns in your training data."
        
        assert not(any((drop_X_valid.dtypes == 'object').values)), \
        "You still need to encode some of the categorical columns in your validation data."

        assert len(drop_X_train.columns) == len(drop_X_valid.columns), \
        ("Please ensure your training and validation data have the same number of columns.")

        assert all(drop_X_train.columns == drop_X_valid.columns), \
        ("Please ensure your training and validation data have the same columns.  You should drop "
         "the same columns in both.")

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
        # check stuff from previous question
        assert not(any((X_train_2.dtypes == 'object').values)), \
        ("It looks like your dataset still contains categorical columns that need to be preprocessed.  Did you use "
         "`X_train_1` and `X_valid_1` as starting points before dealing with missing values?")
        assert len(X_train_2.columns) == len(X_valid_2.columns), \
        "Please ensure your training and validation data have the same number of columns."
        assert all(X_train_2.columns == X_valid_2.columns), \
        "Please ensure your training and validation data have the same column ordering."

        # columns with missing values
        cols_with_missing_train = [col for col in X_train_2.columns if X_train_2[col].isnull().any()]
        cols_with_missing_valid = [col for col in X_valid_2.columns if X_valid_2[col].isnull().any()]
        assert len(cols_with_missing_train) == 0, \
        "It looks like your training set still contains columns with missing data."
        assert len(cols_with_missing_valid) == 0, \
        "It looks like your validation set still contains columns with missing data."

class CardinalityA(EqualityCheckProblem):
    _vars = ['high_cardinality_numcols', 'num_cols_neighborhood']
    _expected = [3, 25]
    _hint = ("To one-hot encode a variable, we need one column for each unique entry.")
    _solution = CS(
"""# How many categorical variables in the training data
# have cardinality greater than 10?
high_cardinality_numcols = 3

# How many columns are needed to one-hot encode the 
# 'Neighborhood' variable in the training data?
num_cols_neighborhood = 25
""")
    
class CardinalityB(EqualityCheckProblem):
    _vars = ['OH_entries_added', 'label_entries_added']
    _expected = [990000, 0]
    _hint = ("To calculate how many entries are added to the dataset through the one-hot encoding, "
             "begin by calculating how many entries are needed to encode the categorical variable "
             "(by multiplying the number of rows by the number of columns in the one-hot encoding). "
             "Then, to obtain how many entries are **added** to the dataset, subtract the number "
             "of entries in the original column.")
    _solution = CS(
"""# How many entries are added to the dataset by 
# replacing the column with a one-hot encoding?
OH_entries_added = 1e4*100 - 1e4

# How many entries are added to the dataset by
# replacing the column with a label encoding?
label_entries_added = 0
""")

class OneHot(CodingProblem):
    _vars = ['OH_X_train', 'OH_X_valid']
    _hint = ("Begin by applying the one-hot encoder to the low cardinality columns in the " 
             "training and validation data in `X_train[low_cardinality_cols]` and "
             "`X_valid[low_cardinality_cols]`, respectively.")
    _solution = CS(
"""# Apply one-hot encoder to each column with categorical data
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(X_train[low_cardinality_cols]))
OH_cols_valid = pd.DataFrame(OH_encoder.transform(X_valid[low_cardinality_cols]))

# One-hot encoding removed index; put it back
OH_cols_train.index = X_train.index
OH_cols_valid.index = X_valid.index

# Remove categorical columns (will replace with one-hot encoding)
num_X_train = X_train.drop(object_cols, axis=1)
num_X_valid = X_valid.drop(object_cols, axis=1)

# Add one-hot encoded columns to numerical features
OH_X_train = pd.concat([num_X_train, OH_cols_train], axis=1)
OH_X_valid = pd.concat([num_X_valid, OH_cols_valid], axis=1)

""")
    
    def check(self, OH_X_train, OH_X_valid):
        
        assert type(OH_X_train) == pd.core.frame.DataFrame, \
        "`OH_X_train` is not a pandas DataFrame."
        
        assert type(OH_X_valid) == pd.core.frame.DataFrame, \
        "`OH_X_valid` is not a pandas DataFrame."

        assert not(any((OH_X_train.dtypes == 'object').values)), \
        "You still need to encode some of the categorical columns in your training data."
        
        assert not(any((OH_X_valid.dtypes == 'object').values)), \
        "You still need to encode some of the categorical columns in your validation data."
        
        assert len(OH_X_train.columns) == 155, \
        "`OH_X_train` should have 155 columns."
        
        assert len(OH_X_valid.columns) == 155, \
        "`OH_X_valid` should have 155 columns."
    
Cardinality = MultipartProblem(CardinalityA, CardinalityB)
    
qvars = bind_exercises(globals(), [
    Drop,
    DealMiss,
    Cardinality, 
    OneHot
    ],
    tutorial_id=-1,
    var_format='step_{n}',
    )
__all__ = list(qvars)
