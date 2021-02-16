import pandas as pd
from category_encoders import MEstimateEncoder

from learntools.core import *

df = pd.read_csv("../input/fe-course-data/ames.csv")


class Q1(ThoughtExperiment):
    _solution = """ The `Neighborhood` feature looks promising. It has the most categories of any feature, and several categories are rare. Others that could be worth considering are `SaleType`, `MSSubClass`, `Exterior1st`, `Exterior2nd`. In fact, almost any of the nominal features would be worth trying because of the prevalence of rare categories."""


class Q2(CodingProblem):
    _hint = """Your code should look something like:
```python
encoder = MEstimateEncoder(
    cols=____,
    m=____,
)


# Fit the encoder on the encoding split
____.____(X_encode, y_encode)

# Encode the training split
X_train = encoder.transform(X_pretrain, y_train)
```
"""
    _solution = CS(
        """
encoder = MEstimateEncoder(
    cols=["Neighborhood"],
    m=1.0,
)


# Fit the encoder on the encoding split
encoder.fit(X_encode, y_encode)

# Encode the training split
X_train = encoder.transform(X_pretrain, y_train)
"""
    )
    _vars = ["encoder", "X_train"]

    def check(self, encoder, X_train):
        assert (
            len(encoder.cols) != 0
        ), "Be sure to choose at least one feature to encode. Include its name in a list with the `cols` argument, like: `cols=[____]`."
        X_solution = self._make_solution(encoder)
        assert_df_equals(X_train, X_solution, name="X_train")

    def _make_solution(self, encoder):
        # Encoding split
        X_encode = df.sample(frac=0.20, random_state=0)
        y_encode = X_encode.pop("SalePrice")
        # Training split
        X_pretrain = df.drop(X_encode.index)
        y_train = X_pretrain.pop("SalePrice")
        # Encoder
        encoder.fit(X_encode, y_encode)
        X_solution = encoder.transform(X_pretrain, y_train)
        return X_solution


class Q3(ThoughtExperiment):
    _hint = """
Suppose you had a dataset like:

| Count | Target |
|-------|--------|
| 0     | 10     |
| 1     | 5      |
| 2     | 30     |
| 3     | 22     |

What is the mean value of Target when Count is equal to 0? It's 10, since 0 only occurs in the first row. So what would be the result of mean-encoding Count, knowing that Count never has any duplicate values?
"""
    _solution = """
Since `Count` never has any duplicate values, the mean-encoded `Count` is essentially an exact copy of the target. In other words, mean-encoding turned a completely meaningless feature into a perfect feature.

Now, the only reason this worked is because we trained XGBoost on the same set we used to train the encoder. If we had used a hold-out set instead, none of this "fake" encoding would have transferred to the training data.

The lesson is that when using a target encoder it's very important to use separate data sets for training the encoder and training the model. Otherwise the results can be very disappointing!
"""


qvars = bind_exercises(globals(), [Q1, Q2, Q3], var_format="q_{n}")
__all__ = list(qvars)
