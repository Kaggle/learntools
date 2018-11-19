import pandas as pd

from learntools.core import *
from learntools.core.asserts import *
from learntools.core.richtext import CodeSolution as CS

reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)

class PointsDtype(EqualityCheckProblem):
    _var = 'dtype'
    _expected = reviews.points.dtype
    _solution = CS("dtype = reviews.points.dtype")

class StrPoints(EqualityCheckProblem):
    _var = 'point_strings'
    _expected = reviews.points.astype(str)
    _solution = CS("point_strings = reviews.points.astype(str)")

class CountMissingPrices(EqualityCheckProblem):
    _var = 'n_missing_prices'
    _expected = reviews.price.isnull().sum()
    _solution = CS("""\
missing_price_reviews = reviews[reviews.price.isnull()]
n_missing_prices = len(missing_price_reviews)
# Cute alternative solution: if we sum a boolean series, True is treated as 1 and False as 0
n_missing_prices = reviews.price.isnull().sum()
# or equivalently:
n_missing_prices = pd.isnull(reviews.price).sum()
""")

class ReviewsPerRegion(EqualityCheckProblem):
    _var = 'reviews_per_region'
    _expected = reviews.region_1.fillna('Unknown').value_counts().sort_values(ascending=False)
    _solution = CS("reviews_per_region = reviews.region_1.fillna('Unknown').value_counts().sort_values(ascending=False)")

qvars = bind_exercises(globals(), [
    PointsDtype,
    StrPoints,
    CountMissingPrices,
    ReviewsPerRegion,
    ],
    tutorial_id=-1,
    )
__all__ = list(qvars)
