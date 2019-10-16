import datetime
import pandas as pd
import numpy as np

from learntools.core import *

class TimeSeriesTrainTestSplit(ThoughtExperiment):
    _solution = \
"""
Since you are dealing with time series data, you'll want to train on an earlier portion and see how the model performs on data from a later time. For example, you can train on data before the start of 2018 and test the model on data from 2018.

This type of split provides a good analog to measure how your model will perform in the future if you train it with data that is available today.
"""

class SelectTrainingData(CodingProblem):
    _var = 'model_data'
    _hint = ''
    _solution = CS(
"""
query = \"""
        SELECT start_station_name,
               TIMESTAMP_TRUNC(start_time, HOUR) as start_hour,
               COUNT(bikeid) as num_rides
        FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
        WHERE start_time < "2018-01-01"
        GROUP BY start_station_name, start_hour
        \"""

query_job = client.query(query)
model_data = query_job.to_dataframe()
""")
    def check(self, perm_obj):
        FIX THIS
        assert np.allclose(perm_obj.feature_importances_,
                            np.array([ 0.62288714,  0.8266946 ,  0.53837499,
                                       0.84735854, -0.00291397]), rtol=0.1)


class CreateFirstBQMLModel(CodingProblem):
    _vars = ['query_job']
    _solution = CS(
"""
data['abs_lon_change'] = abs(data.dropoff_longitude - data.pickup_longitude)
data['abs_lat_change'] = abs(data.dropoff_latitude - data.pickup_latitude)

features_2  = ['pickup_longitude',
               'pickup_latitude',
               'dropoff_longitude',
               'dropoff_latitude',
               'abs_lat_change',
               'abs_lon_change']

X = data[features_2]
new_train_X, new_val_X, new_train_y, new_val_y = train_test_split(X, y, random_state=1)
second_model = RandomForestRegressor(n_estimators=30, random_state=1).fit(new_train_X, new_train_y)

# Create a PermutationImportance object on second_model and fit it to new_val_X and new_val_y
perm2 = PermutationImportance(second_model, random_state=1).fit(new_val_X, new_val_y)

# show the weights for the permutation importance you just calculated
eli5.show_weights(perm2, feature_names = features_2)
""")
    def check(self, perm_obj):
        assert np.allclose(perm_obj.feature_importances_,
                          np.array([0.06128774,  0.08575455, 0.07350467,
                                    0.07330853,  0.57827417, 0.44671882]),
                          rtol=0.1), "That's not right. Check that you set the right seed and used the right data"

class ScaleUpFeatureMagnitude(ThoughtExperiment):
    _solution = """
    The scale of features does not affect permutation importance per se. The only reason that rescaling a feature would affect PI is indirectly, if rescaling helped or hurt the ability of the particular learning method we're using to make use of that feature.
    That won't happen with tree based models, like the Random Forest used here.
    If you are familiar with Ridge Regression, you might be able to think of how that would be affected.
    That said, the absolute change features are have high importance because they capture total distance traveled, which is the primary determinant of taxi fares...It is not an artifact of the feature magnitude.
    """

qvars = bind_exercises(globals(), [
    WhichFeaturesAreUseful,
    FirstPermImportance,
    WhyLatitude,
    ImportanceWithAbsFeatures,
    ScaleUpFeatureMagnitude,
    FromPermImportanceToMarginalEffect
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
