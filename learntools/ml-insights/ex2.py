import datetime
import pandas as pd
import numpy as np
from learntools.core.utils import bind_exercises
from learntools.core.richtext import CodeSolution as CS
from learntools.core.problem import *

class WhichFeaturesAreUseful(ThoughtExperiment):
    _solution = """It would be helpful to know whether New York City taxis
    vary prices based on how many passengers they have. Most places do not
    change fares based on numbers of passengers. If you (correctly) assume New York City is the same, than only the top 4 features should matter. But all of those
    probably matter.
    """

class FirstPermImportance(CodingProblem):
    _vars = ['perm']
    _hint = 'The only thing you need to change is the first argument to `PermutationImportance()`. Find the right model name in the code above'
    _solution = CS(
"""
import eli5
from eli5.sklearn import PermutationImportance

perm = PermutationImportance(first_model, random_state=1).fit(val_X, val_y)
eli5.show_weights(perm, feature_names = base_features)
""")
    def check(self, perm_obj):
        assert np.allcose(perm_obj.feature_importances_, 
                            [ 0.62288714,  0.8266946 ,  0.53837499,  0.84735854, -0.00291397], rtol=0.05)

class WhyLatitude(ThoughtExperiment):
    _solution = """
    1. Travel might tend to have greater latitude distances than longitude distances. If the longitudes values were generally closer together, shuffling them wouldn't matter as much.
    2. Different parts of the city might have different pricing rules (e.g. price per mile). If the divisions correspond more closely to latitude than longitude, that would cause latitude to matter more for accurate price prediction.
    3. Tolls might be greater on roads going North<->South (changing latitude) than
    on roads going East <-> West (changing longitude).  Thus latitude would have a larger effect on the prediction because it captures the amount of the tolls.
    """

class ImportanceWithAbsFeatures(CodingProblem):
    _vars = ['perm2']
    _hint = 'The only thing you need to change is the first argument to `PermutationImportance()`. Find the right model name in the code above'
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
perm2 = PermutationImportance(second_model).fit(new_val_X, new_val_y)

# show the weights for the permutation importance you just calculated
eli5.show_weights(perm2, feature_names = features_2)
""")
    def check(self, perm_obj):
        assert np.allcose(perm.feature_importances_,
                            [ 0.62288714,  0.8266946 ,  0.53837499,  0.84735854, -0.00291397], rtol=0.05)


qvars = bind_exercises(globals(), [
    WhichFeaturesAreUseful,
    FirstPermImportance,
    WhyLatitude
    ],
    # tutorial_id=118,
    var_format='q_{n}',
    )
__all__ = list(qvars)
