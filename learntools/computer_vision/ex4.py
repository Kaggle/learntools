from learntools.core import *
import tensorflow as tf


class Q1A(ThoughtExperiment):
    _solution = ""


class Q1B(ThoughtExperiment):
    _solution = ""

Q1 = MultipartProblem(Q1A, Q1B)

class Q2A(ThoughtExperiment):
    _hint = "Stacking the second layer expanded the receptive field by one neuron on each side, giving $3+1+1=5$ for each dimension. If you expanded by one neuron again, what would you get?"
    _solution = "The third layer would have a $7\times 7$ receptive field."

class Q2B(ThoughtExperiment):
    _hint = "This pooling layer collapses a $2\times 2$ patch into a single pixel, effectively *doubling* the number of connections along each dimension. "
    _solution = "Doubling a $7 \times 7$ field produces a $14 \times 14$ field for the final outputs."

Q2 = MultipartProblem(Q2A, Q2B)


class Q3(CodingProblem):
    _hint = "You just need a list of numbers, maybe three to five."
    _solution = CS("""
kernel = tf.constant([0.1, 0.2, 0.3, 0.4])
""")
    def check(self):
        pass


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
    
