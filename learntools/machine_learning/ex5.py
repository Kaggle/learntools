from numpy import array
import pandas as pd
import sklearn
from sklearn.tree import DecisionTreeRegressor
from learntools.core import *

class BestTreeSize(EqualityCheckProblem):
    _var = 'best_tree_size'
    _expected = 100
    _hint = ("You will call get_mae in the loop. You'll need to map "
             "the names of your data structure to the names in get_mae")
    _solution = CS("""# Here is a short solution with a dict comprehension.
# The lesson gives an example of how to do this with an explicit loop.
scores = {leaf_size: get_mae(leaf_size, train_X, val_X, train_y, val_y) for leaf_size in candidate_max_leaf_nodes}
best_tree_size = min(scores, key=scores.get)
""")


class FitModelWithAllData(CodingProblem):
    _vars = ['final_model', 'X', 'y']
    _hint = 'Fit with the ideal value of max_leaf_nodes. In the fit step, use all of the data in the dataset'
    _solution = CS("""# Fit the model with best_tree_size. Fill in argument to make optimal size
final_model = DecisionTreeRegressor(max_leaf_nodes=best_tree_size, random_state=1)

# fit the final model
final_model.fit(X, y)""")

    def check(self, final_model, X, y):
        assert final_model.max_leaf_nodes == 100, "Didn't set max_leaf_nodes to the right value when building the tree"
        # Model has in-sample R^2 of 0.92 when run on all data, independent of seed.
        # score(X,y) is 0.88 if model was trained on train_X and train_y
        assert final_model.score(X, y) > 0.9, "Your model isn't quite as accurate as expected. Did you fit it on all the data?"
qvars = bind_exercises(globals(), [
    BestTreeSize,
    FitModelWithAllData
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
