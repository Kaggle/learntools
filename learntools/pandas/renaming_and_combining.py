import pandas as pd

from learntools.core import *
from learntools.core.asserts import *
from learntools.core.richtext import CodeSolution as CS

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
    _solution = CS("renamed = reviews.rename(columns=dict(region_1='region', region_2='locale'))")

class RenameIndex(EqualityCheckProblem):
    _var = 'reindexed'
    _expected = reviews.rename_axis('wines', axis='rows')
    _solution = CS("reindexed = reviews.rename_axis('wines', axis='rows')")

class ConcatReddit(EqualityCheckProblem):
    _var = 'combined_products'
    _expected = pd.concat([gaming_products, movie_products])
    _solution = CS("combined_products = pd.concat([gaming_products, movie_products])")

class JoinLifting(EqualityCheckProblem):
    _var = 'powerlifting_combined'
    _expected = powerlifting_meets.set_index("MeetID").join(powerlifting_competitors.set_index("MeetID"))
    _solution = CS('powerlifting_combined = powerlifting_meets.set_index("MeetID").join(powerlifting_competitors.set_index("MeetID"))')

qvars = bind_exercises(globals(), [
    RenameCols,
    RenameIndex,
    ConcatReddit,
    JoinLifting,
    ],
    tutorial_id=50,
    )
__all__ = list(qvars)
