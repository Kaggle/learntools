from learntools.core import *

class Q1(EqualityCheckProblem):
    _var = "pretrained_base.trainable"
    _expected = False
    _hint = ""
    _solution = CS("pretrained_base.trainable = False")


class Q2(CodingProblem):
    _hint = ""
    _solution = CS(
"""
model = Sequential([
    pretrained_base,
    layers.Flatten(),
    layers.Dense(8, activation='relu'),
    layers.Dense(1, activation='sigmoid'),
])
""")
    def check(self):
        # type check `Dense`, attributes, etc.
        pass


class Q3(EqualityCheckProblem):
    _var = "loss"
    _expected = 'binary_crossentropy'
    _hint = ""
    _solution = CS("loss = 'binary_cross_entropy'")


class Q4(ThoughtExperiment):
    _solution = ""
