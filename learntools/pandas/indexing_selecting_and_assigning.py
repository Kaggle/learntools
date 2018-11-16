import pandas as pd

from learntools.core import *
from learntools.core.asserts import *
from learntools.core.richtext import CodeSolution as CS

reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)

class SelectDescCol(EqualityCheckProblem):
    _var = 'desc'
    _expected = (
            reviews.description
    )
    #_solution = CS("desc = reviews.description")
    # This behaviour really should have been opt-in, rather than opt-out :/
    show_solution_on_correct = False
    _solution = """
```python
desc = reviews.description
```
`desc` is a pandas `Series` object, with an index matching the `reviews` DataFrame. 
In general, when we select a single column from a DataFrame, we'll get a Series.
"""

class FirstDesc(EqualityCheckProblem):
    _var = 'first_description'
    _expected = (
            reviews.description.iloc[0]
    )
    _solution = CS("first_description = reviews.description.iloc[0]")

class FirstRow(EqualityCheckProblem):
    _var = 'first_row'
    _expected = (
            reviews.iloc[0]
    )
    _solution = CS("first_row = reviews.iloc[0]")

class FirstDescs(EqualityCheckProblem):
    _var = 'first_descriptions'
    _expected = (
            reviews.description.iloc[:10]
    )
    _solution = CS("first_descriptions = reviews.description.iloc[:10]")

class SampleReviews(EqualityCheckProblem):
    _var = 'sample_reviews'
    indices = [1, 2, 3, 5, 8]
    _expected = (
            reviews.loc[indices],
    )
    _solution = CS("""\
indices = [1, 2, 3, 5, 8]
sample_reviews = reviews.loc[indices]""")

class RowColSelect(EqualityCheckProblem):
    _var = 'df'
    cols = ['country', 'province', 'region_1', 'region_2']
    indices = [0, 1, 10, 100]
    _expected = (
            reviews.loc[indices, cols],
    )
    _solution = CS("""\
cols = ['country', 'province', 'region_1', 'region_2']
indices = [0, 1, 10, 100]
df = reviews.loc[indices, cols]""")

class RowColSelect2(EqualityCheckProblem):
    _var = 'df'
    cols = ['country', 'variety']
    _expected = (
            reviews.head(100).loc[:,cols],
    )
    _solution = CS("""\
cols = ['country', 'variety']
df = reviews.head(100).loc[:,cols]""")

class NMissingPrices(EqualityCheckProblem):
    _var = 'missing_prices'
    _expected = (
            pd.isnull(reviews.price).sum(),
    )
    _solution = CS("""\
missing_price_reviews = reviews[reviews.price.isnull()]
missing_prices = len(missing_price_reviews)
# Cute alternative solution: if we sum a boolean series, True is treated as 1 and False as 0
missing_prices = reviews.price.isnull().sum()
""")

class ItalianWines(EqualityCheckProblem):
    _var = 'italian_wines'
    _expected = (
            reviews[reviews.country == 'Italy'],
    )
    _solution = CS("italian_wines = reviews[reviews.country == 'Italy']")

class TopOceanicWines(EqualityCheckProblem):
    _var = 'top_oceania_wines'
    cols = ['country', 'variety']
    _expected = reviews[
                (reviews.country.isin(['Australia', 'New Zealand']))
                & (reviews.points >= 98)
    ]
    _solution = CS("""\
top_oceania_wines = reviews[
    (reviews.country.isin(['Australia', 'New Zealand']))
    & (reviews.points >= 98)
]""")

qvars = bind_exercises(globals(), [
    SelectDescCol,
    FirstDesc,
    FirstRow,
    FirstDescs,
    SampleReviews,
    RowColSelect,
    RowColSelect2,
    ItalianWines,
    NMissingPrices,
    TopOceanicWines,
    ],
    tutorial_id=-1,
    )
__all__ = list(qvars)
