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
clicks_label = label_encoding_soln()

class LabelEncoding(CodingProblem):
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
    
    def check(self, answer):
        cat_features = ['ip', 'app', 'device', 'os', 'channel']
        for feature in cat_features:
            col = feature + '_labels'
            assert col in list(answer.columns), "{} column is missing".format(col)
            assert set(answer[col]) == set(clicks_label[col]), "{} column does not have the correct values".format(col)

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
