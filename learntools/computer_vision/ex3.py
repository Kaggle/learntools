from learntools.core import *

class Q1(CodingProblem):
    _hint = ""
    _vars = ["kernel"]
    _solution = CS("""
# Your answer might be different, but something like this would work!
kernel = tf.constant([
    [1, 0, 1],
    [0, -4, 0],
    [1, 0, 1],
])
""")
    def check(self, kernel):
        # check class, shape
        pass

class Q2(CodingProblem):
    _hint = ""
    _vars = ["conv2d", "image_filter"]
    _solution = cs("""
conv2d.set_weights(kernel)

image_filter = conv2d(image)
""")
    def check(self, conv2d, image_filter):
        # check weights defined, image_filter is an image at least
        pass

class Q3(CodingProblem):
    _hint = ""
    _vars = ["image_detect"]
    _solution = CS("""
image_detect = relu(image_filter)
""")
    def check(self, image_detect):
        pass

class Q5(CodingProblem):
    _hint = ""
    _vars = ["image_condense"]
    _solution = CS("""
image_condense = maxpool2d
""")
    def check(self, image_condense):
        pass

class Q6(ThoughtExperiment):
    _solution = ""

class Q7(ThoughtExperiment):
    _solution = ""
