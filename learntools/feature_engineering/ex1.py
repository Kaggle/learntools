import pandas as pd
from sklearn import preprocessing

from learntools.core import *

click_data = pd.read_csv('../input/feature-engineering-data/train_sample.csv',
                         parse_dates=['click_time'])

def timestamp_features_soln():
    click_times = click_data['click_time']
    clicks = click_data.assign(day=click_times.dt.day.astype('uint8'),
                               hour=click_times.dt.hour.astype('uint8'), 
                               minute=click_times.dt.minute.astype('uint8'),
                               second=click_times.dt.second.astype('uint8'))
    return clicks

class TimestampFeatures(EqualityCheckProblem):
    _var = 'clicks'
    _hint = ("With a timestamp column in a dataframe, you can get access to "
             "datetime attibutes and functions with the `.dt` attribute. For "
             "example `tscolumn.dt.day` will convert a timestamp column to days")
    _expected = timestamp_features_soln()
    _solution = CS(
    """
    # Split up the times
    click_times = click_data['click_time']
    clicks['day'] = click_times.dt.day.astype('uint8')
    clicks['hour'] = click_times.dt.hour.astype('uint8')
    clicks['minute'] = click_times.dt.minute.astype('uint8')
    clicks['second'] = click_times.dt.second.astype('uint8')
    """)


def label_encoding_soln():
    cat_features = ['ip', 'app', 'device', 'os', 'channel']
    label_encoder = preprocessing.LabelEncoder()
    
    clicks = timestamp_features_soln()
    for feature in cat_features:
        encoded = label_encoder.fit_transform(clicks[feature])
        clicks[feature + '_labels'] = encoded
    return clicks

class LabelEncoding(EqualityCheckProblem):
    _var = 'clicks'
    _hint = ("Try looping through each of the categorical features and using the "
             " using LabelEncoder's .fit_transform method")
    _solution = CS(
    """
    label_encoder = preprocessing.LabelEncoder()
    for feature in cat_features:
        encoded = label_encoder.fit_transform(clicks[feature])
        clicks[feature + '_labels'] = encoded
    """)
    _expected = label_encoding_soln()

class OnehotEncoding(ThoughtExperiment):
    _solution = """
    The `ip` column has 58,000 values, which means it will create an extremely 
    sparse matrix with 58,000 columns. This many columns will make your model run
    very slow, so in general you want to avoid one-hot encoding features with many
    levels. LightGBM models work with label encoded features, so you don't actually need to 
    one-hot encode the categorical features.

    """

class TrainTestSplits(ThoughtExperiment):
    _solution = """
    Since our model is meant to predict events in the future, we must also validate the
    model on events in the future. If the data is mixed up between the training and test 
    sets, then future data will leak in to the model and our validation results will 
    overestimate the performance on new data.
    """

# class CreateSplits(CodingProblem):
#     _vars = ['train', 'valid', 'test']
#     _hint = ("You can sort dataframes with the `.sort_values` method. Then find how many rows "
#              "are 10% of the data (as an integer) and use that to slice the dataframe "
#              "appropriately. You can index starting from the end of the dataframe using negative "
#              "values, for example `df[-1000:]` will return the last 1000 rows.")

#     _solution = CS("""
#     valid_fraction = 0.1
#     sorted_clicks = clicks.sort_values('click_time')
#     valid_rows = int(len(sorted_clicks) * valid_fraction)
#     train = sorted_clicks[:-valid_rows * 2]
#     # valid size == test size, last two sections of the data
#     valid = sorted_clicks[-valid_rows * 2:-valid_rows]
#     test = sorted_clicks[-valid_rows:]
#     """)

#     def check(self, train_, valid_, test_):
#         sorted_clicks = click_data.sort_values('click_time')

#         valid_fraction = 0.1
#         valid_rows = int(len(sorted_clicks) * valid_fraction)
#         train = sorted_clicks[:-valid_rows * 2]
#         # valid size == test size, last two sections of the data
#         valid = sorted_clicks[-valid_rows * 2:-valid_rows]
#         test = sorted_clicks[-valid_rows:]

#         assert train_.shape[0] == train.shape[0], "The train set isn't 80% of the data"
#         assert valid_.shape[0] == valid.shape[0], "The validation set isn't 10% of the data"
#         assert test_.shape[0] == test.shape[0], "The test set isn't 10% of the data"

#         assert (train_['click_time'].values == train['click_time'].values).all(), (""
#             "The click times aren't properly sorted in the train set")
#         assert (valid_['click_time'].values == valid['click_time'].values).all(), (""
#             "The click times aren't properly sorted in the validation set")
#         assert (test_['click_time'].values == test['click_time'].values).all(), (""
#             "The click times aren't properly sorted in the test set")


qvars = bind_exercises(globals(), [
    TimestampFeatures,
    LabelEncoding,
    OnehotEncoding,
    TrainTestSplits,
    # CreateSplits,
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
