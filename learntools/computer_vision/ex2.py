from learntools.core import *
import tensorflow as tf


class Q1(CodingProblem):
    _var = 'kernel'
    _hint = """
Your solution should look something like:
```python
kernel = tf.constant([
    [ _, _, _ ],
    [ _, _, _ ],
    [ _, _, _ ],
])
```
"""
    _solution = CS("""
# This is just one possibility.
kernel = tf.constant([
    [-2, -1, 0],
    [-1, 1, 1],
    [0, 1, 2],
])
""")
    def check(self, kernel):
        assert isinstance(kernel, tf.Tensor), \
            ("Your kernel needs to be a TensorFlow tensor. Be sure to keep the " +
             "`tf.constant` when giving your answer.")

        assert (kernel.dtype.is_floating or kernel.dtype.is_integer), \
            (("You need to define a numeric tensor. Your tensor has type `{}`.")
             .format(kernel.dtype))

        shape = kernel.shape.as_list()
        assert (len(shape) == 2), \
            (("Your kernel needs to have have a shape with only two dimensions, " +
              "but you defined a kernel with shape `{}`, which has `{}` dimensions. " +
              "Be sure to have only one level of nesting in your brackets, like " +
              "`[[1, 2], [3, 4]].` See the kernel in the tutorial for a guide.")
             .format(shape, len(shape)))
        
        assert shape == [3, 3], \
            (("Your kernel needs a shape `[3, 3]`, but yours has shape {}. " +
              "Remember that you need 3 rows and 3 columns.")
              .format(shape))


class Q2(CodingProblem):
    _vars = ['conv_fn']
    _hint = "The function is in the `tf.nn` module."
    _solution = CS("""
conv_fn = tf.nn.conv2d
""")
    def check(self, conv_fn):
        assert conv_fn is tf.nn.conv2d

class Q3(CodingProblem):
    _vars = ['relu_fn']
    _hint = "The function is in the `tf.nn` module.`"
    _solution = CS("relu_fn = tf.nn.relu")

    def check(self, relu_fn):
        assert relu_fn is tf.nn.relu

class Q4(ThoughtExperiment):
    _solution = "In the tutorial, we talked about how the pattern of positive numbers will tell you the kind of features the kernel will extract. This kernel has a vertical column of 1's, and so we would expect it to return features of vertical lines."


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3, Q4,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
