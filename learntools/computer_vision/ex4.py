from learntools.core import *
import tensorflow as tf


class Q1(ThoughtExperiment):
    _hint = r"Stacking the second layer expanded the receptive field by one neuron on each side, giving $3+1+1=5$ for each dimension. If you expanded by one neuron again, what would you get?"
    _solution = r"The third layer would have a $7 \times 7$ receptive field."


qvars = bind_exercises(globals(), [
        Q1,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
    
