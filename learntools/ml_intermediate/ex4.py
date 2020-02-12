import pandas as pd
import sklearn
from sklearn.pipeline import Pipeline

from learntools.core import *

class YourTurnModel(CodingProblem):
    _vars = ['numerical_transformer', 'categorical_transformer', 'model']
    _hint = ("While there are many different potential solutions to this problem, we achieved "
             "satisfactory results by changing only `column_transformer` from the default value - "
             "specifically, we changed the `strategy` parameter that decides how missing "
             "values are imputed.")
    _solution = CS(
"""# Preprocessing for numerical data
numerical_transformer = SimpleImputer(strategy='constant')

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Define model
model = RandomForestRegressor(n_estimators=100, random_state=0)
""")

    def check(self, numerical_transformer, categorical_transformer, model):

        def try_pipeline(transformer):
            try:
                Pipeline(steps=[('transformer', transformer)])
                return True
            except:
                return False

        assert try_pipeline(numerical_transformer) == True, \
        "`numerical_transformer` is not a valid preprocessor."

        assert try_pipeline(categorical_transformer) == True, \
        "`categorical_transformer` is not a valid preprocessor."

        assert type(model) == sklearn.ensemble.RandomForestRegressor, \
        "Please change `model` to a random forest model with scikit-learn."


class YourTurnPredict(CodingProblem):
    _var = 'score'
    _hint = ("Please see the hint from Part A to get some ideas for how to change the "
             "preprocessing steps and model to get better performance.")
    _solution = CS(
"""# Please run the code cell without changes.s
""")

    def check(self, score):
        assert score < 17861, \
        ("Your MAE is too high - please amend `numerical_transformer`, "
         "`categorical_transformer`, and/or `model` from Part A to get better performance.")

YourTurn = MultipartProblem(YourTurnModel, YourTurnPredict)

class TestPreds(CodingProblem):
    _var = 'preds_test'
    _hint = ("Use the pipeline in `my_pipeline` and the `predict()` method.")
    _solution = CS(
"""# Preprocessing of test data, fit model
preds_test = my_pipeline.predict(X_test)
""")

    def check(self, preds_test):
        assert len(preds_test) == 1459, \
        "Did you generate predictions with the test data?"

qvars = bind_exercises(globals(), [
    YourTurn,
    TestPreds
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
