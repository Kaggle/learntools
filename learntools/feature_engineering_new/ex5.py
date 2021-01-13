import pandas as pd
from sklearn.cluster import KMeans

from learntools.core import *

df = pd.read_csv("../input/fe-course-data/ames.csv")


class Q1(ThoughtExperiment):
    _solution = """The first component, `PC1`, seems to be a kind of "size" component, similar to what we saw in the tutorial: all of the features have the same sign (positive), indicating that this component is describing a contrast between houses having large values and houses having small values for these features.

The interpretation of the third component `PC3` is a little trickier. The features `GarageArea` and `YearRemodAdd` both have near-zero loadings, so let's ignore those. This component is mostly about `TotalBsmtSF` and `GrLivArea`. It describes a contrast between houses with a lot of living area but small (or non-existant) basements, and the opposite: small houses with large basements.
"""


class Q2(CodingProblem):
    _hint = """Try using the `make_mi_scores` function on `X_pca` to find out which components might have the most potential. Then look at the loadings to see what kinds of relationships among the features might be important.

Alternatively, you could use the components themselves. Try joining the highest scoring components from `X_pca` to `X`, or just join all of `X_pca` to `X`.
"""
    _solution = """Here are two possible solutions, though you might have been able to find others.
```python
# Solution 1: Inspired by loadings
X = df.copy()
y = X.pop("SalePrice")

X["Feature1"] = X.GrLivArea + X.TotalBsmtSF
X["Feature2"] = X.YearRemodAdd * X.TotalBsmtSF

score = score_dataset(X, y)
print(f"Your score: {score:.5f} RMSLE")


# Solution 2: Uses components
X = df.copy()
y = X.pop("SalePrice")

X = X.join(X_pca)
score = score_dataset(X, y)
print(f"Your score: {score:.5f} RMSLE")
```
"""
    _var = "score"

    def check(self, score):
        assert (
            score < 0.140
        ), f"You need a score less than `0.140` RMSLE. You got `{score:.5f}` RMSLE"


class Q3(ThoughtExperiment):
    _hint = ""
    _solution = """Notice that there are several dwellings listed as `Partial` sales in the `Edwards` neighborhood that stand out. A partial sale is what occurs when there are multiple owners of a property and one or more of them sell their "partial" ownership of the property.

These kinds of sales are often happen during the settlement of a family estate or the dissolution of a business and aren't advertised publicly. If you were trying to predict the value of a house on the open market, you would probably be justified in removing sales like these from your dataset -- they are truly outliers.
"""


qvars = bind_exercises(globals(), [Q1, Q2, Q3], var_format="q_{n}")
__all__ = list(qvars)
