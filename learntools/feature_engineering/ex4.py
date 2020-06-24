import pandas as pd

from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from learntools.core import *

def get_data_splits(dataframe, valid_fraction=0.1):

    dataframe = dataframe.sort_values('click_time')
    valid_rows = int(len(dataframe) * valid_fraction)
    train = dataframe[:-valid_rows * 2]
    # valid size == test size, last two sections of the data
    valid = dataframe[-valid_rows * 2:-valid_rows]
    test = dataframe[-valid_rows:]

    return train, valid, test

class FeatureSelectionData(ThoughtExperiment):
    _solution = ("Including validation and test data within the feature "
                 "selection is a source of leakage. You'll want to perform "
                 "feature selection on the train set only, then use the results "
                 "there to remove features from the validation and test sets.")

class UnivariateSelection(CodingProblem):
    _vars = ['train', 'dropped_columns']
    _hint = ("Create the selector with `SelectKBest` using `f_classif` as the scoring "
             "function. The `.fit_transform` method will return an array with the "
             "best features retained. However, it doesn't retain the column names "
             "so you'll need to get them back. The easiest way is to use "
             "`selector.inverse_transform(X_new)` to get back an array with the same "
             "shape as the original features but with the dropped columns zeroed out. "
             "From this you can build a DataFrame with the same index and columns as the "
             "original features. From here, you can find the names of the dropped columns "
             "by finding all the columns with a variance of zero.")
    _solution = CS("""
    # Do feature extraction on the training data only!
    selector = SelectKBest(f_classif, k=40)
    X_new = selector.fit_transform(train[feature_cols], train['is_attributed'])

    # Get back the features we've kept, zero out all other features
    selected_features = pd.DataFrame(selector.inverse_transform(X_new),
                                    index=train.index,
                                    columns=feature_cols)

    # Dropped columns have values of all 0s, so var is 0, drop them
    dropped_columns = selected_features.columns[selected_features.var() == 0]""")

    def check(self, train, dropped_columns_):

        assert dropped_columns_.shape[0] == 51, "Please choose to keep 40 columns"

        feature_cols = train.columns.drop(['click_time', 'attributed_time', 'is_attributed'])
        # Do feature extraction on the training data only!
        selector = SelectKBest(f_classif, k=40)
        X_new = selector.fit_transform(train[feature_cols], train['is_attributed'])

        # Get back the features we've kept, zero out all other features
        selected_features = pd.DataFrame(selector.inverse_transform(X_new),
                                         index=train.index,
                                         columns=feature_cols)

        # Dropped columns have values of all 0s, so var is 0, drop them
        dropped_columns = selected_features.columns[selected_features.var() == 0]

        message = ("Somethings not right with your result. Be sure to use the train "
                   "dataset for the feature selection")

        assert (dropped_columns == dropped_columns_).all(), message


class BestKValue(ThoughtExperiment):
    _solution = ("To find the best value of K, you can fit multiple models with "
                 "increasing values of K, then choose the smallest K with validation "
                 "score above some threshold or some other criteria. A good way to "
                 "do this is loop over values of K and record the validation scores "
                 "for each iteration.")

class L1Regularization(CodingProblem):
    _vars = ['select_features_l1', 'train']
    _hint = ("First fit the logistic regression model, then pass it to `SelectFromModel`. "
             "That should give you a model with the selected features, you can get the "
             "selected features with `X_new = model.transform(X)`. However, this leaves off the "
             "column labels so you'll need to get them back. The easiest way to do this "
             "is to use `model.inverse_transform(X_new)` to get back the original `X` array "
             "with the dropped columns as all zeros. Then you can create a new DataFrame "
             "with the index and columns of `X`. From there, keep the columns that aren't "
             "all zeros.")
    _solution = CS("""
    def select_features_l1(X, y):
        logistic = LogisticRegression(C=0.1, penalty="l1", random_state=7, solver='liblinear').fit(X, y)
        model = SelectFromModel(logistic, prefit=True)

        X_new = model.transform(X)

        # Get back the kept features as a DataFrame with dropped columns as all 0s
        selected_features = pd.DataFrame(model.inverse_transform(X_new),
                                        index=X.index,
                                        columns=X.columns)

        # Dropped columns have values of all 0s, keep other columns
        cols_to_keep = selected_features.columns[selected_features.var() != 0]

        return cols_to_keep""")

    def check(self, student_func, train):
        def select_features_l1(X, y):
            logistic_model = LogisticRegression(C=0.1,
                                                penalty="l1",
                                                random_state=7,
                                               solver='liblinear').fit(X, y)
            model = SelectFromModel(logistic_model, prefit=True)

            X_new = model.transform(X)

            # Get back the kept features as a DataFrame with dropped columns as all 0s
            selected_features = pd.DataFrame(model.inverse_transform(X_new),
                                            index=X.index,
                                            columns=X.columns)

            # Dropped columns have values of all 0s, keep other columns
            cols_to_keep = selected_features.columns[selected_features.var() != 0]

            return cols_to_keep

        feature_cols = train.columns.drop(['click_time', 'attributed_time',
                                           'is_attributed'])

        n_samples = 10000
        X, y = train[feature_cols][:n_samples], train['is_attributed'][:n_samples]

        selected = select_features_l1(X, y)
        selected_student = student_func(X, y)

        assert selected_student is not ____, "Please implement `select_features_l1`"

        message = ("Your result isn't quite right. Make sure you're using a logistic "
                  "regression model with an l1 penalty. Set the random state to 7 and "
                  "the regularization parameter to 0.1.")
        assert selected.equals(selected_student), message




class FeatureSelectionTrees(ThoughtExperiment):
    _solution = ("You could use something like `RandomForestClassifier` or "
                 "`ExtraTreesClassifier` to find feature importances. "
                 "`SelectFromModel` can use the feature importances to find the "
                 "best features.")


class L1SelectionTopK(ThoughtExperiment):
    _solution = ("To select a certain number of features with L1 regularization, "
                 "you need to find the regularization parameter that leaves the "
                 "desired number of features. To do this you can iterate over models with "
                 "different regularization parameters from low to high and choose the "
                 "one that leaves K features. Note that for the scikit-learn models "
                 "C is the *inverse* of the regularization strength.")


qvars = bind_exercises(globals(), [
    FeatureSelectionData,
    UnivariateSelection,
    BestKValue,
    L1Regularization,
    FeatureSelectionTrees,
    L1SelectionTopK
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
