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

class FirstPermImportance(EqualityCheckProblem):
    _vars = ['perm']
    max_year_built = 2010
    min_home_age = datetime.datetime.now().year - max_year_built
    _expected = np.array([0.62288714, 0.8266946, 0.84735854, -0.00291397])
    _hint = 'The only thing you need to change is the first argument to `PermutationImportance()`. Find the right model name in the code above'
    _solution = CS(
"""
import eli5
from eli5.sklearn import PermutationImportance

perm = PermutationImportance(first_model, random_state=1).fit(val_X, val_y)
eli5.show_weights(perm, feature_names = base_features)
""")

TODO: Add questions 3 and 4 HERE

qvars = bind_exercises(globals(), [
    WhichFeaturesAreUseful,
    FirstPermImportance,
    ],
    # tutorial_id=118,
    var_format='q_{n}',
    )
__all__ = list(qvars)
