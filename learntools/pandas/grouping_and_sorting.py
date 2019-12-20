import pandas as pd

from learntools.core import *

reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)

class ReviewsWritten(EqualityCheckProblem):
    _var = 'reviews_written'
    _expected = reviews.groupby('taster_twitter_handle').size()
    _hint = "Use the `groupby` operation and `size()` (or `count()`)."
    _solution = """
```python
reviews_written = reviews.groupby('taster_twitter_handle').size()
```
or
```python
reviews_written = reviews.groupby('taster_twitter_handle').taster_twitter_handle.count()
```
"""

class BestRatingPerPrice(EqualityCheckProblem):
    _var = 'best_rating_per_price'
    _expected = reviews.groupby('price')['points'].max().sort_index()
    _hint = "Use `max()` and `sort_index()`.  The relevant columns in the DataFrame are `price` and `points`."
    _solution = CS("best_rating_per_price = reviews.groupby('price')['points'].max().sort_index()")

class PriceExtremes(EqualityCheckProblem):
    _var = 'price_extremes'
    _expected = reviews.groupby('variety').price.agg([min, max])
    _hint = "Use `agg()`."
    _solution = CS("price_extremes = reviews.groupby('variety').price.agg([min, max])")

class SortedVarieties(EqualityCheckProblem):
    _var = 'sorted_varieties'
    _expected = reviews.groupby('variety').price.agg([min, max]).sort_values(by=['min', 'max'], ascending=False)
    _hint = "Use `sort_values()`, and provide a list of names to sort by."
    _solution = CS("sorted_varieties = price_extremes.sort_values(by=['min', 'max'], ascending=False)")

class ReviewerMeanRatings(EqualityCheckProblem):
    _var = 'reviewer_mean_ratings'
    _expected = reviews.groupby('taster_name').points.mean()
    _hint = "Use `mean()`."
    _solution = CS("reviewer_mean_ratings = reviews.groupby('taster_name').points.mean()")

class GroupbyCountryVariety(EqualityCheckProblem):
    _var = 'country_variety_counts'
    _expected = reviews.groupby(['country', 'variety']).size().sort_values(ascending=False)
    _hint = "Use `groupby()`, and provide a list of columns to group by.  You may also find `size()` and `sort_values()` to be useful!"
    _solution = CS("country_variety_counts = reviews.groupby(['country', 'variety']).size().sort_values(ascending=False)")

qvars = bind_exercises(globals(), [
    ReviewsWritten,
    BestRatingPerPrice,
    PriceExtremes,
    SortedVarieties,
    ReviewerMeanRatings,
    GroupbyCountryVariety,
    ],
    )
__all__ = list(qvars)
