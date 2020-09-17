from learntools.core import *


class Q1(ThoughtExperiment):
    _solution = "The gap between these curves is quite small and the validation loss never increases, so it's more likely that the network is underfitting."

class Q2(ThoughtExperiment):
    _solution = "Now the validation loss begins to rise very early, while the training loss continues to decrease. This indicates that the network has begun to overfit. At this point, we would need to try something to prevent it, either by reducing the number of units or through a method like early stopping. (We'll see another in the next lesson!)"

class Q3(CodingProblem):
    _hint = ""
    _solution = CS("")
    _var = "early_stopping"
    def check(self, early_stopping):
        assert(early_stopping.patience == 5), \
            ("The `patience` argument should be 5.")
        assert(early_stopping.min_delta == -0.001), \
            ("The `min_delta` argument should be 0.001.")
        assert(early_stopping.restore_best_weights), \
            ("The `restore_best_weights` argument should be `True`.")

class Q4(ThoughtExperiment):
    _solution = "The early stopping callback did stop the training once the network began overfitting. Moreover, by including `restore_best_weights` we still get to keep the model where validation loss was lowest."
    

qvars = bind_exercises(globals(), [
        Q1, Q2, Q3, Q4,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
