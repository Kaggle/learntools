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
        
        assert shape == [3, 3] \
            (("Your kernel needs a shape `[3, 3]`, but yours has shape {}. " +
              "Remember that you need 3 rows and 3 columns.")
              .format(shape))


class Q2(CodingProblem):
    _vars = ['image_filter']
    _hint = """
Your solution should look something like:
```python
image_filter = tf.nn.conv2d(
    input=____,
    filters=____,
    strides=1,
    padding='VALID',
)
```
"""
    _solution = CS("""
image_filter = tf.nn.conv2d(
    input=image,
    filters=kernel,
    strides=1, # or (1, 1)
    padding='VALID',
)
""")
    def check(self, image_filter):
        # Default size defined in the exercise.
        size = [398, 398]
        image_size = tf.squeeze(image_filter).shape.as_list()
        assert image_size == size, \
            (("The size of `image_filter` should be `{}`, but actually is `{}`." +
              "Did you use `padding='VALID'` and `strides=1`?")
             .format(size, image_size))


class Q3(CodingProblem):
    _vars = ['image_detect']
    _hint = """
Your solution should look something like:
```python
image_detect = tf.nn.relu(____)
```
"""
    _solution = CS("""
image_detect = tf.nn.relu(image_filter)
""")

    def check(self, image_detect):
        assert isinstance(image_detect, tf.Tensor), \
            (("`image_detect` should be the output of `tf.nn.relu`, which " +
              " is a `tf.Tensor`. You have `image_detect` as a `{}`. Did " +
              " you use the `tf.nn.relu` function?")
             .format(image_detect.__class__.__name__))
        assert tf.reduce_min(image_detect).numpy() >= 0.0, \
            ("All the values of `image_detect` should be greater than or " +
             "equal to 0. Did you use the `tf.nn.relu` function?")


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
