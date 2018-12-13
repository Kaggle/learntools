import pandas as pd

from learntools.core import *

reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)

class StaticDeliciousColumn(EqualityCheckProblem):
    # This doesn't validate that they actually modified the original copy
    # we gave them rather than creating a new object and reassigning r to it.
    # But I don't think that's a mistake people are likely to make.
    _var = 'r'
    r = reviews.copy()
    r['is_delicious'] = "yes"
    _expected = r
    _solution = CS("r['is_delicious'] = \"yes\"")

qvars = bind_exercises(globals(), [
    StaticDeliciousColumn,
    ],
    tutorial_id=-1,
)
__all__ = list(qvars)
