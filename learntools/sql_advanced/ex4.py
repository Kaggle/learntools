from learntools.core import *

class PetCostumes(EqualityCheckProblem):
    _var = 'query_to_optimize'
    _expected = 3
    _hint = ("Do the queries run on big or small datasets?  Do they need to be run many times, or just once?  Is the data "
             "spread over multiple tables, or contained in just one?")
    _solution = \
"""
`query_to_optimize = 3`

Why **3**: Because data is sent for each costume at each second, this is the query that is likely to involve the most data (by far). And it will be run on a recurring basis. So writing this well could pay off on a recurring basis.

Why not **1**: This is the second most valuable query to optimize. It will be run on a recurring basis, and it involves merges, which is commonly a place where you can make your queries more efficient

Why not **2**: This sounds like it will be run only one time. So, it probably doesn’t matter if it takes a few seconds extra or costs a few cents more to run that one time. Also, it doesn’t involve JOINs. While the data has text fields (the reviews), that is the data you need. So, you can’t leave these out of your select query to save computation.
"""

class Mitzie(ThoughtExperiment):
    _hint = ("Does the dataset have a lot of missing values, or just a few?  Would we lose much "
             "information if we completely ignored the columns with missing entries?")
    _solution = ("Since there are relatively few missing entries in the data (the column with "
                 "the greatest percentage of missing values is missing less than 20% of its entries), "
                 "we can expect that dropping columns is unlikely to yield good results.  This is "
                 "because we'd be throwing away a lot of valuable data, and so imputation will likely "
                 "perform better.")


qvars = bind_exercises(globals(), [
    PetCostumes,
    Mitzie
    ],
    tutorial_id=-1,
    var_format='q_{n}',
    )

__all__ = list(qvars)
