import pandas as pd

from learntools.core import *

reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)

# Load some other datasets used in this exercise
gaming_products = pd.read_csv("../input/things-on-reddit/top-things/top-things/reddits/g/gaming.csv")
gaming_products['subreddit'] = "r/gaming"
movie_products = pd.read_csv("../input/things-on-reddit/top-things/top-things/reddits/m/movies.csv")
movie_products['subreddit'] = "r/movies"

powerlifting_meets = pd.read_csv("../input/powerlifting-database/meets.csv")
powerlifting_competitors = pd.read_csv("../input/powerlifting-database/openpowerlifting.csv")

class RenameCols(EqualityCheckProblem):
    _var = 'renamed'
    _expected = reviews.rename(columns=dict(region_1='region', region_2='locale'))
    _hint = "Use `rename()`, and specify a `columns` parameter."
    _solution = CS("renamed = reviews.rename(columns=dict(region_1='region', region_2='locale'))")

class RenameIndex(EqualityCheckProblem):
    _var = 'reindexed'
    _expected = reviews.rename_axis('wines', axis='rows')
    _hint = "Use the `rename_axis()` method."
    _solution = CS("reindexed = reviews.rename_axis('wines', axis='rows')")

class ConcatReddit(CodingProblem):
    _var = 'combined_products'
    _solution = CS("combined_products = pd.concat([gaming_products, movie_products])")
    _hint = "Use `pd.concat()`"
    
    def check(self, combined_products):
        _expected = pd.concat([gaming_products, movie_products])
        _expected2 = pd.concat([movie_products, gaming_products])
        assert (combined_products.equals(_expected) or combined_products.equals(_expected2)), ("Incorrect value for DataFrame `combined_products`")

class JoinLifting(CodingProblem):
    _var = 'powerlifting_combined'
    _solution = CS('powerlifting_combined = powerlifting_meets.set_index("MeetID").join(powerlifting_competitors.set_index("MeetID"))')
    _hint = "Use `pd.Dataframe.join()`."
    
    def check(self, powerlifting_combined):
        _expected = powerlifting_meets.set_index("MeetID").join(powerlifting_competitors.set_index("MeetID"))
        _expected2 = powerlifting_competitors.set_index("MeetID").join(powerlifting_meets.set_index("MeetID"))
        assert (powerlifting_combined.equals(_expected) or powerlifting_combined.equals(_expected2)), ("Incorrect value for DataFrame `powerlifting_combined`")
    
    

qvars = bind_exercises(globals(), [
    RenameCols,
    RenameIndex,
    ConcatReddit,
    JoinLifting,
    ],
    )
__all__ = list(qvars)
