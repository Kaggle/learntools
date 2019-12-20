import pandas as pd

from learntools.core import *

class InvestigateEquality(EqualityCheckProblem):
    _vars = ['num_rows', 'num_cols_with_missing', 'tot_missing']
    _expected = [1168, 3, 276]
    _hint = ("Use the output of `X_train.shape` to get the number of rows and columns in "
             "the training data.  The `missing_val_count_by_column` Series has an entry "
             "for each column in the data, and the output above prints the number of "
             "missing entries for each column with at least one missing entry.")
    _solution = CS(
"""# How many rows are in the training data?
num_rows = 1168

# How many columns in the training data have missing values?
num_cols_with_missing = 3

# How many missing entries are contained in all of the training data?
tot_missing = 212 + 6 + 58
""")

class InvestigateThought(ThoughtExperiment):
    _hint = ("Does the dataset have a lot of missing values, or just a few?  Would we lose much "
             "information if we completely ignored the columns with missing entries?")
    _solution = ("Since there are relatively few missing entries in the data (the column with "
                 "the greatest percentage of missing values is missing less than 20% of its entries), "
                 "we can expect that dropping columns is unlikely to yield good results.  This is "
                 "because we'd be throwing away a lot of valuable data, and so imputation will likely "
                 "perform better.")

Investigate = MultipartProblem(InvestigateEquality, InvestigateThought)

class DropMissing(CodingProblem):
    _vars = ['reduced_X_train', 'reduced_X_valid']
    _hint = ("Begin by finding the list of columns in the data with missing values.  Then, drop "
             "these columns in both the training and validation data with the `drop()` method.")
    _solution = CS(
"""# Get names of columns with missing values
cols_with_missing = [col for col in X_train.columns
                     if X_train[col].isnull().any()]

# Drop columns in training and validation data
reduced_X_train = X_train.drop(cols_with_missing, axis=1)
reduced_X_valid = X_valid.drop(cols_with_missing, axis=1)
""")

    def check(self, reduced_X_train, reduced_X_valid):
        assert type(reduced_X_train) == pd.core.frame.DataFrame, \
        "`reduced_X_train` is not a pandas DataFrame."

        assert type(reduced_X_valid) == pd.core.frame.DataFrame, \
        "`reduced_X_valid` is not a pandas DataFrame."

        assert len([col for col in reduced_X_train.columns
                    if reduced_X_train[col].isnull().any()]) == 0, \
        "`reduced_X_train` still contains missing values."

        assert len([col for col in reduced_X_valid.columns
                    if reduced_X_valid[col].isnull().any()]) == 0, \
        "`reduced_X_valid` still contains missing values."

        assert reduced_X_train.shape == (1168, 33), \
        "`reduced_X_train` should have shape (1168, 33)."

        assert reduced_X_valid.shape == (292, 33), \
        "`reduced_X_train` should have shape (292, 33)."

        cols_with_missing = ['LotFrontage', 'MasVnrArea', 'GarageYrBlt']
        assert all([col not in reduced_X_train.columns for col in cols_with_missing]), \
        ("Your training data contains some column names that should have been dropped from "
         "the original dataset.")

        assert all([col not in reduced_X_valid.columns for col in cols_with_missing]), \
        ("Your validation data contains some column names that should have been dropped from "
         "the original dataset.")

class ImputeCode(CodingProblem):
    _vars = ['imputed_X_train', 'imputed_X_valid']
    _hint = ("Begin by defining an instance of the `SimpleImputer()` class.  Then, use the imputer "
             "to fit and transform the training data, before transforming the validation data. "
             "Get the original column names from the original DataFrames `X_train` and `X_valid`.")
    _solution = CS(
"""# Imputation
my_imputer = SimpleImputer()
imputed_X_train = pd.DataFrame(my_imputer.fit_transform(X_train))
imputed_X_valid = pd.DataFrame(my_imputer.transform(X_valid))

# Imputation removed column names; put them back
imputed_X_train.columns = X_train.columns
imputed_X_valid.columns = X_valid.columns
""")

    def check(self, imputed_X_train, imputed_X_valid):
        assert type(imputed_X_train) == pd.core.frame.DataFrame, \
        "`imputed_X_train` is not a pandas DataFrame."

        assert type(imputed_X_valid) == pd.core.frame.DataFrame, \
        "`imputed_X_valid` is not a pandas DataFrame."

        assert len([col for col in imputed_X_train.columns
                    if imputed_X_train[col].isnull().any()]) == 0, \
        "`imputed_X_train` still contains missing values."

        assert len([col for col in imputed_X_valid.columns
                    if imputed_X_valid[col].isnull().any()]) == 0, \
        "`imputed_X_valid` still contains missing values."

        assert imputed_X_train.shape == (1168, 36), \
        "`imputed_X_train` should have shape (1168, 36)."

        assert imputed_X_valid.shape == (292, 36), \
        "`imputed_X_train` should have shape (292, 36)."

        assert 'LotFrontage' in imputed_X_train.columns, \
        "Did you put the column names back in `imputed_X_train`?"

        assert 'LotFrontage' in imputed_X_valid.columns, \
        "Did you put the column names back in `imputed_X_valid`?"

        assert round(imputed_X_train['LotFrontage'].mean()) == 70, \
        "Did you impute with the mean value along each column?"

        assert round(imputed_X_valid['LotFrontage'].mean()) != 72, \
        ("Did you fit the transform to the validation data?  Please instead fit the transform "
         "to the training data, and then use the fitted transform to impute the values in the "
         "validation data.")

class ImputeThought(ThoughtExperiment):
    _hint = ("Did removing missing values yield a larger or smaller MAE than imputation? "
             "Does this agree with the coding example from the tutorial?")
    _solution = ("Given that thre are so few missing values in the dataset, we'd expect imputation "
                 "to perform better than dropping columns entirely.  However, we see that dropping "
                 "columns performs slightly better!  While this can probably partially be attributed "
                 "to noise in the dataset, another potential explanation is that the imputation method "
                 "is not a great match to this dataset.  That is, maybe instead of filling in the "
                 "mean value, it makes more sense to set every missing value to a value of 0, to fill "
                 "in the most frequently encountered value, or to use some other method.  For "
                 "instance, consider the `GarageYrBlt` column (which indicates the year that the "
                 "garage was built).  It's likely that in some cases, a "
                 "missing value could indicate a house that does not have a garage.  Does it make "
                 "more sense to fill in the median value along each column in this case?  Or could we "
                 "get better results by filling in the minimum value along each column?  It's not "
                 "quite clear what's best in this case, but perhaps we can rule out some options immediately - "
                 "for instance, setting missing values in this column to 0 is likely to yield horrible results!")

Impute = MultipartProblem(ImputeCode, ImputeThought)

class PredsCodeA(CodingProblem):
    _vars = ['final_X_train', 'final_X_valid']
    _hint = ("Use any approach of your choosing to deal with missing values in the data.  For inspiration, "
             "check out the code from the tutorial!")
    _solution = CS(
"""# Imputation
final_imputer = SimpleImputer(strategy='median')
final_X_train = pd.DataFrame(final_imputer.fit_transform(X_train))
final_X_valid = pd.DataFrame(final_imputer.transform(X_valid))

# Imputation removed column names; put them back
final_X_train.columns = X_train.columns
final_X_valid.columns = X_valid.columns
""")

    def check(self, final_X_train, final_X_valid):
        assert type(final_X_train) == pd.core.frame.DataFrame, \
        "`final_X_train` is not a pandas DataFrame."

        assert type(final_X_valid) == pd.core.frame.DataFrame, \
        "`final_X_valid` is not a pandas DataFrame."

        assert len([col for col in final_X_train.columns
                    if final_X_train[col].isnull().any()]) == 0, \
        "`final_X_train` still contains missing values."

        assert len([col for col in final_X_valid.columns
                    if final_X_valid[col].isnull().any()]) == 0, \
        "`final_X_valid` still contains missing values."

        assert final_X_train.shape[1] == final_X_valid.shape[1], \
        "`final_X_train` and `final_X_valid` do not have the same number of columns."

        assert len(final_X_train) == 1168, \
        "`final_X_train` should have 1168 rows (one for each entry in `y_train`)."

        assert len(final_X_valid) == 292, \
        "`final_X_valid` should have 292 rows (one for each entry in `y_valid`)."

class PredsCodeB(CodingProblem):
    _vars = ['final_X_test', 'preds_test']
    _hint = ("After preprocessing the test data, you can get the model's predictions by using `model.predict()`.")
    _solution = CS(
"""# Preprocess test data
final_X_test = pd.DataFrame(final_imputer.transform(X_test))

# Get test predictions
preds_test = model.predict(final_X_test)
""")

    def check(self, final_X_test, preds_test):
        assert type(final_X_test) == pd.core.frame.DataFrame, \
        "`final_X_test` is not a pandas DataFrame."

        assert len([col for col in final_X_test.columns
                    if final_X_test[col].isnull().any()]) == 0, \
        "`final_X_test` still contains missing values."

        assert len(final_X_test) == 1459, \
        "`final_X_test` should have 1459 rows (one for each row in `X_test`)."

PredsCode = MultipartProblem(PredsCodeA, PredsCodeB)

qvars = bind_exercises(globals(), [
    Investigate,
    DropMissing,
    Impute,
    PredsCode
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
