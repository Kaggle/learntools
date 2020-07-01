from learntools.core import *
import tensorflow as tf


class Q1(CodingProblem):
    _var = 'kernel'
    _hint = CS("""
# Your solution should look something like:
kernel = tf.constant([
    [ numbers ],
    [ numbers ],
    [ numbers ],
])
""")
    _solution = CS("""
# This is just one possibility.
kernel = tf.constant([
    [-2, -1, 0],
    [-1, 1, 1],
    [0, 1, 2],
])
""")
    def check(self, kernel):
        assert (isinstance(kernel, tf.Tensor))
        assert ((len(kernel.shape) == 2),
                ("Your kernel needs to have have a shape with only two dimensions, " +
                 "but you defined a kernel with shape {}, which has {} dimensions. " +
                 "You should have only one level of nesting in your brackets, like " +
                 "`[[1, 2], [3, 4]].` See the kernel in the tutorial for a guide."))

class Q2(CodingProblem):
    _vars = ['image_filter', 'image']
    _hint = CS("""
# Your solution should look something like:
image_filter = tf.nn.conv2d(
    input=____,
    filters=____,
    strides=____,
    padding=____,
)
""")
    _solution = CS("""
image_filter = tf.nn.conv2d(
    input=image,
    filters=kernel,
    strides=1,
    padding='SAME',
)
""")
    def check(self, image_filter, image):
        assert ((image_filter.shape == image.shape),
                ("Using the settings in the tutorial, the shapes of `image_filter`" +
                 "and `image` should be the same. The shape of `image` is {} while " +
                 "the shape of `image_filter` is {}. Did you use 'SAME' for padding " +
                 "and keep the strides at 1?".filter(image.shape, image_filter.shape)))


class Q3(CodingProblem):
    _vars = ['image_detect', 'image_filter', 'image']
    _hint = CS("""
# Your solution should look something like:
image_detect = tf.nn.relu(____)
""")
    _solution = CS("""
image_detect = tf.nn.relu(image_filter)
""")        
    def check(self, image_detect, image_filter, image):
        assert((image_detect != tf.nn.relu(image)),
               ("It looks like you might have applied the ReLU to `image` instead " +
                "of `image_filter`. Remember that the input to ReLU is the output " +
                "of the convolution."))


class Q4A(CodingProblem):
    _hint = ""
    _solution = ""
    def check(self):
        pass

class Q4B(ThoughtExperiment):
    _solution = "In the tutorial, we talked about how the pattern of positive numbers will tell you the kind of features the kernel will extract. This kernel has a vertical column of 1's, and so we would expect it to return features of vertical lines."

class Q4C(CodingProblem):    
    _hint = ""
    _solution = ""
    def check(self):
        pass

Q4 = MultipartProblem(Q4A, Q4B, Q4C)


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3, Q4,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
