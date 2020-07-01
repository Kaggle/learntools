from learntools.core import *
import tensorflow as tf

class Q1(CodingProblem):
    _vars = ['image_condense', 'image_detect', 'image_filter', 'image']
    _hint = ""
    _solution = CS("""
image_filter = tf.nn.conv2d(
    input=image,
    filters=kernel,
    strides=1,
    padding='SAME',
)
""")
    def check(self, image_condense, image_detect, image_filter, image):
        pass
    # TODO: check that the shape shrinks and that image_condense is
    # max pooled image_detect


class Q2(ThoughtExperiment):
    _solution = ""

class Q3(ThoughtExperiement):
    _solution = ""


class Q4A(CodingProblem):
    _hint = ""
    _solution = ""
    def check(self):
        pass

class Q4B(CodingProblem):
    _hint = ""
    _solution = ""
    def check(self):
        pass
    
class Q4C(ThoughtExperiment):
    _solution = ""

Q4 = MultipartProblem(Q4A, Q4B, Q4C)


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3, Q4,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
