import pandas as pd

from learntools.core import *

df = pd.read_csv("../input/fe-course-data/ames.csv")


class Q1(EqualityCheckProblem):
    _hint = """Try looking at the data documentation, which you can see by running:
```
!cat "../input/fe-course-data/DataDocumentation.txt"
```
"""
    _solution = CS(
        """
overall_qual = "ordinal"
central_air = "binary"
gr_liv_area = "continuous"
neighborhood = "nominal"
fireplaces = "discrete"
"""
    )
    _vars = [
        "overall_qual",
        "central_air",
        "gr_liv_area",
        "neighborhood",
        "fireplaces",
    ]
    _expected = [
        "ordinal",
        "binary",
        "continuous",
        "nominal",
        "discrete",
    ]


class Q2(ThoughtExperiment):
    _solution = "There **does** appear to be a significant relationship between `YearBuilt` and `SalePrice`, but **not** between `MoSold` and `SalePrice`. The relationship between `YearBuilt` and `SalePrice` does not appear to be linear; you would get a better fit with a curve bending upwards from left to right, for instance."


class Q3(CodingProblem):
    _hint = "To find a total you do want to create a sum of some sort. But is a half-bath worth as much as a full-bath? Could it make sense to weight them differently?"
    _solution = """
Either of these would give better results than a simple sum:

```python
X = df.copy()
y = X.pop('SalePrice')

# Solution 1: HalfBath with half the weight of FullBath
X["TotalBaths"] = \
    df.FullBath + 0.5 * df.HalfBath + \
    df.BsmtFullBath + 0.5 * df.BsmtHalfBath

# Solution 2: Same, but preserves int type
X["TotalBaths"] = \
    2 * df.FullBath + df.HalfBath + \
    2 * df.BsmtFullBath + df.BsmtHalfBath
```
"""
    _var = "X"

    def check(self, X):
        soln_1 = (
            df.FullBath
            + 0.5 * df.HalfBath
            + df.BsmtFullBath
            + 0.5 * df.BsmtHalfBath
        )
        soln_2 = (
            2 * df.FullBath
            + df.HalfBath
            + 2 * df.BsmtFullBath
            + df.BsmtHalfBath
        )
        incorrect = (
            df.FullBath + df.HalfBath + df.BsmtFullBath + df.BsmtHalfBath
        )
        assert (
            X["TotalBaths"] != incorrect
        ).any(), "Maybe a weighted sum would be better? How much would you guess a `HalfBath` is worth compared to a `FullBath`?"
        assert (X["TotalBaths"] == soln_1).all() or (
            X["TotalBaths"] == soln_2
        ).all(), "Incorrect value for `{}`".format("X['TotalBaths']")


class Q4(ThoughtExperiment):
    _solution = "Since our error metric RMSLE decreased after adding `TotalBaths` to the feature set, it appears `TotalBaths` is worth keeping."


qvars = bind_exercises(globals(), [Q1, Q2, Q3, Q4], var_format="q_{n}")
__all__ = list(qvars)
