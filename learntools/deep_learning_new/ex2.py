import numpy as np
import tensorflow as tf

from learntools.core import *

# Using *Concrete* dataset
inputs = 8

# Building Sequential Models
class Q1A(CodingProblem):
    _var = "input_shape"
    _expected = [inputs]
    _hint = "Remember to *only* count the input features when determining `input_shape`. You should not count the target (the `quality` column)."
    _solution = CS("""
input_shape = [{inputs}]
# you could also use a 1-tuple, like input_shape = ({inputs},)
""".format(inputs=inputs))
    def check(self, input_shape):
        assert (len(input_shape) == 1), \
            ("""You should use a list of length 1 here. Each entry in the `input_shape` list says how many input values you have in that dimension. The inputs here are numbers (one dimensional) and so your answer should look something like:
```python
input_shape = [____]
```
""")
        assert (input_shape[0] == inputs), \
            ("""Remember that you should *not* count the target when determining the value for `input_shape`. How many columns are there excluding `quality`?
""")

class Q1B(CodingProblem):
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
    layers.Dense(512, activation='relu', input_shape=input_shape),
    layers.Dense(512, activation='relu'),
    layers.Dense(512, activation='relu'),    
    layers.Dense(1),
])
""".format(inputs))
    _var = "model"
    def check(self, model):
        assert (len(model.layers) == 1), \
            ("Your model should have only one layer, a `Dense` layer.")
        
        dense_layer = model.layers[0]
        layer_class = dense_layer.__class__.__name__
        assert (layer_class == "Dense"), \
            ("The only layer in this model should be a `Dense` layer")
        assert (dense_layer.units == 1), \
            ("Your layer should have only a single unit: `units=1`.")
        assert (dense_layer.input_shape == (None, inputs)), \
            ("Your model should have {} inputs. Make sure you answered the previous question correctly!".format(inputs))

class Q1C(CodingProblem):
    hint = ""
    solution = ""
    def check(self):
        pass

Q1 = MultipartProblem(Q1A, Q1B, Q1C)        


# Activation Functions
class Q2A(CodingProblem):
    _hidden_units = 32
    hint = """Your model should look something like:
```python
model = keras.Sequential([
    layers.Dense(____),
    layers.Activation(____),
    layers.Dense(____),
    layers.Activation(____),
    layers.Dense(1),
])
```
"""
    solution = CS("""
model = keras.Sequential([
    layers.Dense(32, input_shape=[8]),
    layers.Activation('relu'),
    layers.Dense(32),
    layers.Activation('relu'),
    layers.Dense(1),
])
q_2.a.assert_check_passed()
""")
    _var = "model"
    def check(self, model):

        layer_classes = [layer.__class__.__name__ for layer in model.layers]
        true_classes = ['Dense', 'Activation', 'Dense', 'Activation', 'Dense']
        assert (layer_classes == true_classes), \
            ("Your model doesn't have the correct kinds of layers. You should have five layers with classes: Dense, Activation, Dense, Activation, Dense.")

        assert (model.layers[0].input_shape == (None, 8)), \
            ("Your model should have 8 inputs. Did you include the input shape to the first layer?")

        dense_activations = [layer.activation.__name__ for layer in model.layers]
        true_activations = ['linear', 'relu', 'linear', 'relu', 'linear']
        assert (dense_activations == true_activations), \
            ("Your model doesn't have the correct activations. The `Dense` layers should be linear (that is, no activation), while the `Activation` layers should be `'relu'`")


class Q2B(CodingProblem):
    hint = ""
    solution = ""
    def check(self):
        pass

Q2 = MultipartProblem(Q2A, Q2B)



qvars = bind_exercises(globals(), [
        Q1, Q2,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)



