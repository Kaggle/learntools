import numpy as np
import tensorflow as tf

from learntools.core import *

# Using *Concrete* dataset
inputs = 8

# Building Sequential Models
class Q1(CodingProblem):
    _var = "input_shape"
    _expected = [inputs]
    _hint = "Remember to *only* count the input features when determining `input_shape`. You should not count the target (the `CompressiveStrength` column)."
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
            ("""Remember that you should *not* count the target when determining the value for `input_shape`. How many columns are there excluding `CompressiveStrength`?
""")


# Define a Model
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
    layers.Dense(512, activation='relu', input_shape=input_shape),
    layers.Dense(512, activation='relu'),
    layers.Dense(512, activation='relu'),    
    layers.Dense(1),
])
""")
    _var = "model"
    def check(self, model):
        assert (len(model.layers) == 4), \
            ("Your model should four layers in all. The first three are the hidden layers and the last is the output layer. The output layer looks like `layers.Dense(1)`.")
        dense_layer = model.layers[0]
        layer_class = dense_layer.__class__.__name__
        layer_classes = [layer.__class__.__name__ for layer in model.layers]
        true_classes = ['Dense', 'Dense', 'Dense', 'Dense']
        # Check layer class
        assert (layer_classes == true_classes), \
            ("Your model doesn't have the correct kinds of layers. You should have five layers with classes: Dense, Dense, Dense, Dense.")
        # Check input shape
        try:
            input_shape = dense_layer.input_shape
        except:
            input_shape = None
        assert (input_shape == (None, inputs)), \
            ("Your model should have {} inputs. Make sure you answered the previous question correctly!".format(inputs))
        # Check activation functions
        dense_activations = [layer.activation.__name__ for layer in model.layers]
        true_activations = ['relu', 'relu', 'relu', 'linear']
        assert (dense_activations == true_activations), \
            ("Your model doesn't have the correct activations. The hidden `Dense` layers should be have `'relu'` activation, while the output layer should be linear (no activation).")

        # Check number of units
        layer_units = [layer.units for layer in model.layers]
        true_units = [512, 512, 512, 1]
        assert (layer_units == true_units), \
            ("Your model doesn't have the correct number of units. The units of the `Dense` layers should be 512, 512, 512, and 1, in that order.")       


# Activation Functions
class Q3(CodingProblem):
    _hidden_units = 32
    _hint = """Your model should look something like:
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
    _solution = CS("""
model = keras.Sequential([
    layers.Dense(32, input_shape=[8]),
    layers.Activation('relu'),
    layers.Dense(32),
    layers.Activation('relu'),
    layers.Dense(1),
])
""")
    _var = "model"
    def check(self, model):

        layer_classes = [layer.__class__.__name__ for layer in model.layers]
        true_classes = ['Dense', 'Activation', 'Dense', 'Activation', 'Dense']
        assert (layer_classes == true_classes), \
            ("Your model doesn't have the correct kinds of layers. You should have five layers with classes: Dense, Activation, Dense, Activation, Dense.")

        try:
            input_shape = model.layers[0].input_shape
        except:
            input_shape = None
        assert (input_shape == (None, 8)), \
            ("Your model should have 8 inputs. Did you include the input shape to the first layer?")
        dense_activations = [layer.activation.__name__ for layer in model.layers]
        true_activations = ['linear', 'relu', 'linear', 'relu', 'linear']
        assert (dense_activations == true_activations), \
            ("Your model doesn't have the correct activations. The `Dense` layers should be linear (that is, no activation), while the `Activation` layers should be `'relu'`")
        # Check number of units
        layer_units = [layer.units for layer in model.layers
                       if layer.__class__.__name__ is 'Dense']
        true_units = [32, 32, 1]
        assert (layer_units == true_units), \
            ("Your model doesn't have the correct number of units. The units in the `Dense` layers should be 32, 32, and 1, in that order.")


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)



