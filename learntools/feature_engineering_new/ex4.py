import pandas as pd
from sklearn.cluster import KMeans

from learntools.core import *

df = pd.read_csv("../input/fe-course-data/ames.csv")


class Q1(ThoughtExperiment):
    _solution = """
1. No, since rescaling would distort the natural distances described by Latitude and Longitude.
2. Either choice could be reasonable, but because the living area of a home tends to be more valuable per square foot, it would make sense to rescale these features so that lot area isn't weighted in the clustering out of proportion to its effect on `SalePrice`, if that is what you were trying to predict.
3. Yes, since these don't have comparable units. Without rescaling, the number of doors in a car (usually 2 or 4) would have negligible weight compared to its horsepower (usually in the hundreds).

What you should take away from this is that the decision of whether and how to rescale features is rarely automatic -- it will usually depend on some domain knowledge about your data and what you're trying to predict. Comparing different rescaling schemes through cross-validation can also be helpful. (You might like to check out the `preprocessing` module in scikit-learn for some of the rescaling methods it offers.)
"""


class Q2(CodingProblem):
    _hint = """ Your code should look something like:
```python
X = df.copy()
y = X.pop("SalePrice")


# YOUR CODE HERE: Define a list of the features to be used for the clustering
features = [
    "LotArea",
    ____,
    ____,
    ____,
    ____,
]

# Standardize
X_scaled = X.loc[:, features]
X_scaled = (X_scaled - X_scaled.mean(axis=0)) / X_scaled.std(axis=0)


# YOUR CODE HERE: Fit the KMeans model to X_scaled and create the cluster labels
kmeans = KMeans(n_clusters=____, n_init=____, random_state=0)
X["Cluster"] = kmeans.fit_predict(____)
```
"""
    _solution = CS(
        """
X = df.copy()
y = X.pop("SalePrice")

features = [
    "LotArea",
    "TotalBsmtSF",
    "FirstFlrSF",
    "SecondFlrSF",
    "GrLivArea",
]

# Standardize
X_scaled = X.loc[:, features]
X_scaled = (X_scaled - X_scaled.mean(axis=0)) / X_scaled.std(axis=0)

kmeans = KMeans(n_clusters=10, n_init=10, random_state=0)
X["Cluster"] = kmeans.fit_predict(X_scaled)
"""
    )
    _var = "X"

    def check(self, X):
        X_solution = self._make_solution()
        assert len(X_solution.columns) == len(
            X.columns
        ), f"Columns are incorrect. You should have {list(X_solution.columns)}. You gave {list(X.columns)}"
        assert sorted(X_solution.columns) == sorted(
            X.columns
        ), f"Columns are incorrect. You should have {list(X_solution.columns)}. You gave {list(X.columns)}"
        assert (
            X_solution.Cluster == X.Cluster
        ).all(), "Cluster labels are incorrect or missing."

    def _make_solution(self):
        X = df.copy()
        X.pop("SalePrice")
        features = [
            "LotArea",
            "TotalBsmtSF",
            "FirstFlrSF",
            "SecondFlrSF",
            "GrLivArea",
        ]

        # Standardize
        X_scaled = X.loc[:, features]
        X_scaled = (X_scaled - X_scaled.mean(axis=0)) / X_scaled.std(axis=0)
        kmeans = KMeans(n_clusters=10, n_init=10, random_state=0)
        X["Cluster"] = kmeans.fit_predict(X_scaled)
        return X


class Q3(CodingProblem):
    _hint = """Your code should look something like:
```python
kmeans = KMeans(n_clusters=10, n_init=10, random_state=0)

X_cd = kmeans.____(X_scaled)

# Label features and join to dataset
X_cd = pd.DataFrame(X_cd, columns=[f"Centroid_{i}" for i in range(X_cd.shape[1])])
X = X.join(X_cd)
```
"""
    _solution = CS(
        """
kmeans = KMeans(n_clusters=10, n_init=10, random_state=0)

# YOUR CODE HERE: Create the cluster-distance features using `fit_transform`
X_cd = kmeans.fit_transform(X_scaled)

# Label features and join to dataset
X_cd = pd.DataFrame(X_cd, columns=[f"Centroid_{i}" for i in range(X_cd.shape[1])])
X = X.join(X_cd)
"""
    )
    _var = "X_cd"

    def check(self, X_cd):
        X_solution = self._make_solution()
        assert (
            (X_solution.round(2).eq(X_cd.round(2))).all().all()
        ), "Cluster-distance features are incorrect or missing."

    def _make_solution(self):
        X = df.copy()
        X.pop("SalePrice")

        features = [
            "LotArea",
            "TotalBsmtSF",
            "FirstFlrSF",
            "SecondFlrSF",
            "GrLivArea",
        ]

        # Standardize
        X_scaled = X.loc[:, features]
        X_scaled = (X_scaled - X_scaled.mean(axis=0)) / X_scaled.std(axis=0)
        kmeans = KMeans(n_clusters=10, n_init=10, random_state=0)
        X_solution = kmeans.fit_transform(X_scaled)
        X_solution = pd.DataFrame(
            X_solution,
            columns=[f"Centroid_{i}" for i in range(X_solution.shape[1])],
        )
        return X_solution


qvars = bind_exercises(globals(), [Q1, Q2, Q3], var_format="q_{n}")
__all__ = list(qvars)
