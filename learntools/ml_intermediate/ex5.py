import pandas as pd
import warnings

from learntools.core import *

class GetScore(FunctionProblem):
    _var = 'get_score'
    _test_cases = [
            (10, 19427.64019542396),
            (20, 18682.264022049276),
    ]
    _hint = ("Begin by making a pipeline with the `Pipeline` class. Be sure to set the "
             "value for `n_estimators` in `RandomForestRegressor()` to the argument supplied to the "
             "`get_score` function. Then, use `cross_val_score()` to get the MAE for each fold, "
             "and take the average. Be sure to set the number of folds to three through the `cv`"
             "parameter.")
    _solution = CS(
"""def get_score(n_estimators):
    my_pipeline = Pipeline(steps=[
        ('preprocessor', SimpleImputer()),
        ('model', RandomForestRegressor(n_estimators, random_state=0))
    ])
    scores = -1 * cross_val_score(my_pipeline, X, y,
                                  cv=3,
                                  scoring='neg_mean_absolute_error')
    return scores.mean()
""")


class GetDict(CodingProblem):
    _var = 'results'
    _hint = ("Begin by instantiating the dictionary with `results = {}`. Then loop over the value "
             "for `n_estimators` that will be plugged into the `get_score()` function, and use the "
             "result to set the value in the dictionary.")
    _solution = CS(
"""results = {}
for i in range(1,9):
    results[50*i] = get_score(50*i)
""")

    def check(self, results):

        # columns with missing values
        assert type(results) == dict, \
        "`results` does not appear to be a Python dictionary."

        assert len(results) == 8, \
        "`results` should have 8 entries, one for each tested value of `n_estimators`."

        assert list(results.keys()) == [50*i for i in range(1,9)], \
        ("The keys in `results` do not appear to be correct.  Please ensure you have one key for each "
         "of 50, 100, 150, ..., 300, 350, 400.")

        assert [round(i) for i in list(results.values())] == [18354, 18395, 18289, 18248,
                                                              18255, 18275, 18270, 18270], \
        ("Some of your average MAE scores appear to be incorrect.  Please use the `get_score()` "
         "function from Step 1 to fill in the dictionary values.")

class BestEst(CodingProblem):
    _var = 'n_estimators_best'
    _hint = ("Find the key corresponding to the minimum value in the `results` dictionary "
             "from the previous step.  This will tell you which value for `n_estimators` "
             "gets the lowest average MAE.")
    _solution = CS("n_estimators_best = min(results, key=results.get)")

    def check(self, n_estimators):
        assert n_estimators < 18000, \
        ("It looks like you have provided an average MAE value.  Please instead provide a value for "
         "`n_estimators` that indicates the ideal number of trees to use in the model. Your answer "
         "should be one of 50, 100, 150, ..., 300, 350, 400.")

        assert n_estimators in [50*i for i in range(1,9)], \
        "Your answer should be one of 50, 100, 150, ..., 300, 350, 400."

        assert n_estimators != 100, \
        ("You should find the value for `n_estimators` with the minimum score, not the maximum score.")

        assert n_estimators == 200, \
        ("Find the key corresponding to the minimum value in the `results` dictionary.")

qvars = bind_exercises(globals(), [
    GetScore,
    GetDict,
    BestEst
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
