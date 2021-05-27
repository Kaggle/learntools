import numpy as np
import tensorflow as tf
from learntools.core import *

# Using *Red Wine Quality* dataset
inputs = 11

# Linear Models
class Q1(CodingProblem):
    _var = "input_shape"
    _hint = "Remember to *only* count the input features when determining `input_shape`. You should not count the target (the `quality` column)."
    _solution = CS("""
input_shape = [{inputs}]
# you could also use a 1-tuple, like input_shape = ({inputs},)
""".format(inputs=inputs))
    def check(self, input_shape):
        assert (type(input_shape) in [list, tuple]), \
            ("""The input shape should be a list (or tuple) with a single integer, like `[__]`.""")
        assert (len(input_shape) == 1), \
            ("""You should use a list of length 1 here. Each entry in the `input_shape` list says how many input values you have in that dimension. The inputs here are numbers (one dimensional) and so your answer should look something like:
```python
input_shape = [____]
```
""")
        assert (input_shape[0] == inputs), \
            ("""Remember that you should *not* count the target when determining the value for `input_shape`. How many columns are there excluding `quality`?
""")

class Q2(CodingProblem):
    _hint = """Your answer should look something like:
```python
model = keras.Sequential([
    ____
])
```
"""
    _solution = CS("""
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    layers.Dense(units=1, input_shape=[{}])
])
""".format(inputs))
    _var = "model"
    def check(self, model):
        assert (len(model.layers) == 1), \
            ("Your model should have only one layer, a `Dense` layer.")
        
        dense_layer = model.layers[0]
        layer_class = dense_layer.__class__.__name__
        try:
            input_shape = dense_layer.input_shape
        except:
            input_shape = None
        assert (layer_class == "Dense"), \
            ("The only layer in this model should be a `Dense` layer")
        assert (dense_layer.units == 1), \
            ("Your layer should have only a single unit: `units=1`.")
        assert (input_shape == (None, inputs)), \
            ("Your model should have {} inputs. Make sure you answered the previous question correctly!".format(inputs))


# Weights and Biases
class Q3(CodingProblem):
    _hint = "You can get the attribute of an object using the 'dot' notation: like `object.attribute`."
    _solution = CS(r"""
# Uncomment if you need the model from the previous question:
# model = keras.Sequential([
#     layers.Dense(units=1, input_shape=[11])
# ])

w, b = model.weights

print("Weights\n{}\n\nBias\n{}".format(w, b))
""")
    _correct_message = """Do you see how there's one weight for each input (and a bias)? Notice though that there doesn't seem to be any pattern to the values the weights have. Before the model is trained, the weights are set to random numbers (and the bias to 0.0). A neural network learns by finding better values for its weights.
"""
    _vars = ['w', 'b']
    def check(self, w, b):
        assert (type(w) is not np.ndarray), \
            ("""Use the `weights` attribute (which returns tensors) instead of the `get_weights` method (which returns a Numpy array).
""")
        assert (tf.is_tensor(w) and tf.is_tensor(b)), \
            ("""The weights `w` and `b` should be tensors. Your answer should be something like:
```python
w, b = model.____
```
""")
        assert (w.shape == tf.TensorShape([inputs, 1])), \
            ("""Your weight tensor `w` doesn't have the correct shape. Make sure you're using the model defined previously, with {} inputs and 1 unit.""".format(inputs))


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
