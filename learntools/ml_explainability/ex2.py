import datetime
import pandas as pd
import numpy as np

from learntools.core.utils import bind_exercises
from learntools.core.problem_factories import simple_problem
from learntools.core.richtext import CodeSolution as CS
from learntools.core.problem import *

class WhichFeaturesAreUseful(ThoughtExperiment):
    _solution = """It would be helpful to know whether New York City taxis
    vary prices based on how many passengers they have. Most places do not
    change fares based on numbers of passengers.
    If you assume New York City is the same, than only the top 4 features listed should matter. At first glance, it seems all of those should matter equally.
    """

class FirstPermImportance(CodingProblem):
    _var = 'perm'
    _hint = 'The only thing you need to change is the first argument to `PermutationImportance()`. Find the right model name in the code above'
    _solution = CS(
"""
import eli5
from eli5.sklearn import PermutationImportance

perm = PermutationImportance(first_model, random_state=1).fit(val_X, val_y)
eli5.show_weights(perm, feature_names = base_features)
""")
    def check(self, perm_obj):
        assert np.allclose(perm_obj.feature_importances_,
                            np.array([ 0.62288714,  0.8266946 ,  0.53837499,
                                       0.84735854, -0.00291397]), rtol=0.1)

class WhyLatitude(ThoughtExperiment):
    _solution = """
    1. Travel might tend to have greater latitude distances than longitude distances. If the longitudes values were generally closer together, shuffling them wouldn't matter as much.
    2. Different parts of the city might have different pricing rules (e.g. price per mile), and pricing rules could vary more by latitude than longitude.
    3. Tolls might be greater on roads going North<->South (changing latitude) than on roads going East <-> West (changing longitude).  Thus latitude would have a larger effect on the prediction because it captures the amount of the tolls.
    """

class ImportanceWithAbsFeatures(CodingProblem):
    _vars = ['perm2']
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
                          rtol=0.1)

class ScaleUpFeatureMagnitude(ThoughtExperiment):
    _solution = """
    The scale of features does not affect permutation importance per se. The only reason that rescaling a feature would affect PI is indirectly, if rescaling helped or hurt the ability of the particular learning method we're using to make use of that feature.
    That won't happen with tree based models, like the Random Forest used here.
    If you are familiar with Ridge Regression, you might be able to think of how that would be affected.
    That said, the absolute change features are have high importance because they capture total distance traveled, which is the primary determinant of taxi fares...It is not an artifact of the feature magnitude.
    """

class FromPermImportanceToMarginalEffect(ThoughtExperiment):
    _solution = """
    We cannot tell from the permutation importance results whether traveling a fixed latitudinal distance is more or less expensive than traveling the same longitudinal distance.
    Possible reasons latitude feature are more important than longitude features
    1. latitudinal distances in the dataset tend to be larger
    2. it is more expensive to travel a fixed latitudinal distance
    3. Both of the above
    If abs_lon_change values were very small, longitues could be less important to the model even if the cost per mile of travel in that direction were high.
    """

qvars = bind_exercises(globals(), [
    WhichFeaturesAreUseful,
    FirstPermImportance,
    WhyLatitude,
    ImportanceWithAbsFeatures,
    ScaleUpFeatureMagnitude,
    FromPermImportanceToMarginalEffect
    ],
    tutorial_id=131,
    var_format='q_{n}',
    )
__all__ = list(qvars)
