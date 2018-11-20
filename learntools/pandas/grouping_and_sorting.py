import pandas as pd

from learntools.core import *
from learntools.core.asserts import *
from learntools.core.richtext import CodeSolution as CS

reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)

class ReviewsWritten(EqualityCheckProblem):
    _var = 'reviews_written'
    _expected = reviews.groupby('taster_twitter_handle').size()
    _solution = CS("reviews_written = reviews.groupby('taster_twitter_handle').size()")

class BestRatingPerPrice(EqualityCheckProblem):
    _var = 'best_rating_per_price'
    _expected = reviews.groupby('price')['points'].max().sort_index()
    _solution = CS("best_rating_per_price = reviews.groupby('price')['points'].max().sort_index()")

class PriceExtremes(EqualityCheckProblem):
    _var = 'price_extremes'
    _expected = reviews.groupby('variety').price.agg([min, max])
    _solution = CS("price_extremes = reviews.groupby('variety').price.agg([min, max])")

class SortedVarieties(EqualityCheckProblem):
    _var = 'sorted_varieties'
    _expected = reviews.groupby('variety').price.agg([min, max]).sort_values(by=['min', 'max'], ascending=False)
    _solution = CS("sorted_varieties = price_extremes.sort_values(by=['min', 'max'], ascending=False)")

class ReviewerMeanRatings(EqualityCheckProblem):
    _var = 'reviewer_mean_ratings'
    _expected = reviews.groupby('taster_name').points.mean()
    _solution = CS("reviewer_mean_ratings = reviews.groupby('taster_name').points.mean()")

class GroupbyCountryVariety(EqualityCheckProblem):
    _var = 'country_variety_counts'
    _expected = reviews.groupby(['country', 'variety']).size().sort_values(ascending=False)
    _solution = CS("country_variety_counts = reviews.groupby(['country', 'variety']).size().sort_values(ascending=False)")

qvars = bind_exercises(globals(), [
    ReviewsWritten,
    BestRatingPerPrice,
    PriceExtremes,
    SortedVarieties,
    ReviewerMeanRatings,
    GroupbyCountryVariety,
    ],
    tutorial_id=48,
    )
__all__ = list(qvars)
