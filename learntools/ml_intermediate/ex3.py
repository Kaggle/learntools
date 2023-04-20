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

        assert drop_X_train.shape[1] == 33, \
        ("`drop_X_train` should have 33 columns.")

        assert drop_X_valid.shape[1] == 33, \
        ("`drop_X_valid` should have 33 columns.")

class LabelA(ThoughtExperiment):
    _hint = ("Are there any values that appear in the validation data but not in the training data?")
    _solution = ("Fitting an ordinal encoder to a column in the training data creates a corresponding "
                 "integer-valued label for each unique value **that appears in the training data**. In "
                 "the case that the validation data contains values that don't also appear in the "
                 "training data, the encoder will throw an error, because these values won't have an "
                 "integer assigned to them.  Notice that the `'Condition2'` "
                 "column in the validation data contains the values `'RRAn'` and `'RRNn'`, but these "
                 "don't appear in the training data -- thus, if we try to use an ordinal encoder with "
                 "scikit-learn, the code will throw an error.")

class LabelB(CodingProblem):
    _vars = ['label_X_train', 'label_X_valid']
    _hint = ("Use the `OrdinalEncoder` class from scikit-learn. You should only encode the columns in "
             "`good_label_cols`.")
    _solution = CS(
"""# Drop categorical columns that will not be encoded
label_X_train = X_train.drop(bad_label_cols, axis=1)
label_X_valid = X_valid.drop(bad_label_cols, axis=1)

# Apply ordinal encoder
ordinal_encoder = OrdinalEncoder()
label_X_train[good_label_cols] = ordinal_encoder.fit_transform(X_train[good_label_cols])
label_X_valid[good_label_cols] = ordinal_encoder.transform(X_valid[good_label_cols])
""")

    def check(self, label_X_train, label_X_valid):

        assert type(label_X_train) == pd.core.frame.DataFrame, \
        "`label_X_train` is not a pandas DataFrame."

        assert type(label_X_valid) == pd.core.frame.DataFrame, \
        "`label_X_valid` is not a pandas DataFrame."

        assert not(any((label_X_train.dtypes == 'object').values)), \
        "You still need to encode some of the categorical columns in your training data."

        assert not(any((label_X_valid.dtypes == 'object').values)), \
        "You still need to encode some of the categorical columns in your validation data."
        
        # remove 45 after nb update
        assert label_X_train.shape[1] in [57, 45], \
        "`label_X_train` does not have the correct number of columns."

        # remove 45 after nb update
        assert label_X_valid.shape[1] in [57, 45], \
        "`label_X_valid` does not have the correct number of columns."

Label = MultipartProblem(LabelA, LabelB)

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
# replacing the column with an ordinal encoding?
label_entries_added = 0
""")

Cardinality = MultipartProblem(CardinalityA, CardinalityB)

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

# Ensure all columns have string type
OH_X_train.columns = OH_X_train.columns.astype(str)
OH_X_valid.columns = OH_X_valid.columns.astype(str)
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
        
        assert list(OH_X_train.index.values)[:10] != list(range(10)), \
        "Remember that one-hot encoding removes the index from your data!  Don't forget to re-add it."


qvars = bind_exercises(globals(), [
    Drop,
    Label,
    Cardinality,
    OneHot
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
