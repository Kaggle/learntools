import pandas as pd

from learntools.core import *

reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)

class PointsDtype(EqualityCheckProblem):
    _var = 'dtype'
    _expected = reviews.points.dtype
    _hint = "`dtype` is an attribute of a DataFrame or Series."
    _solution = CS("dtype = reviews.points.dtype")

class StrPoints(EqualityCheckProblem):
    _var = 'point_strings'
    _expected = reviews.points.astype(str)
    _hint = "Convert a column of one type to another by using the `astype` function."
    _solution = CS("point_strings = reviews.points.astype(str)")

class CountMissingPrices(EqualityCheckProblem):
    _var = 'n_missing_prices'
    _expected = reviews.price.isnull().sum()
    _hint = "Use `pd.isnull()`."
    _solution = CS("""\
missing_price_reviews = reviews[reviews.price.isnull()]
n_missing_prices = len(missing_price_reviews)
# Cute alternative solution: if we sum a boolean series, True is treated as 1 and False as 0
n_missing_prices = reviews.price.isnull().sum()
# or equivalently:
n_missing_prices = pd.isnull(reviews.price).sum()
""")
    

class ReviewsPerRegion(CodingProblem):
    _solution = CS("reviews_per_region = reviews.region_1.fillna('Unknown').value_counts().sort_values(ascending=False)")
    _hint = "Use `fillna()`, `value_counts()`, and `sort_values()`."
    _var = 'reviews_per_region'
    
    def check(self, reviews_per_region):
        _expected = reviews.region_1.fillna('Unknown').value_counts().sort_values(ascending=False)
        assert all(reviews_per_region.values == _expected.values), ('Create a Series counting the number of times each value occurs in the `region_1` field.  Replace missing values with `Unknown`, and sort in descending order.')
        

qvars = bind_exercises(globals(), [
    PointsDtype,
    StrPoints,
    CountMissingPrices,
    ReviewsPerRegion,
    ],
    )
__all__ = list(qvars)
