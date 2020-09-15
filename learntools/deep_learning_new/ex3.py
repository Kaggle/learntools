from learntools.core import *

_inputs = 50

# Data Preparation
class Q1(CodingProblem):
    _hint = ""
    _solution = ""
    def check(self):
        pass

class Q2(CodingProblem):
    _var = "input_shape"
    _hints = [
        "Think about whether you should look at the processed data `X_train` or the original data `fuel`.",
        "You should look at the processed data `X_train`, since that is the data actually going into the network. Since the target was already removed, you can just look at the second entry in `X_train.shape` (the columns) to find the number of features."
    ]
    _solution = CS("""
input_shape = [{inputs}]
# or,
input_shape = [X_train.shape[1]]
""".format(inputs=_inputs))

    def check(self, input_shape):
        assert (type(input_shape) [list, tuple]), \
            ("""The input shape should be a list (or tuple) with a single integer, like `[__]`.""")
        assert (input_shape[0] not in [13, 14]), \
            ("Look at the columns of `X_train` for the number of input features, since `X_train` (the processed data) is what is actually being used as input.")
        assert (len(input_shape) == 1), \
            ("""You should use a list of length 1 here. Each entry in the `input_shape` list says how many input values you have in that dimension. The inputs here are numbers (one dimensional) and so your answer should look something like:
```python
input_shape = [____]
```
""")
        assert (input_shape[0] == _inputs), \
            ("The number of inputs should be {good_inputs}, but you gave {bad_inputs}".format(good_inputs=_inputs, bad_inputs=input_shape[0]))


# Fuel Economy Prediction
class Q3(CodingProblem):
    _hint = """Your answer should look something like:
```python
model = keras.Sequential([
    # Hidden layers
    layers.Dense(____),
    layers.Dense(____),
    layers.Dense(____),
    # Output layer
    layers.Dense(1),
])
```
"""
    _solution = CS("""
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=input_shape),
    layers.Dense(64, activation='relu'),
    layers.Dense(64, activation='relu'),    
    layers.Dense(1),
])
""".format(_inputs))
    _var = "model"
    def check(self, model):
        assert (len(model.layers) == 4), \
            ("Your model should four layers in all. The first three are the hidden layers and the last is the output layer. The output layer looks like `layers.Dense(1)`.")
        dense_layer = model.layers[0]
        layer_class = dense_layer.__class__.__name__
        layer_classes = [layer.__class__.__name__ for layer in model.layers]
        true_classes = ['Dense', 'Dense', 'Dense', 'Dense']
        assert (layer_classes == true_classes), \
            ("Your model doesn't have the correct kinds of layers. You should have five layers with classes: Dense, Activation, Dense, Activation, Dense.")
        your_inputs = model.layers[0].input_shape[0]
        assert (your_inputs == _inputs), \
            ("Your model should have {} inputs, but you gave {}.".format(_inputs, your_inputs))
        dense_activations = [layer.activation.__name__ for layer in model.layers]
        true_activations = ['relu', 'relu', 'relu', 'linear']
        assert (dense_activations == true_activations), \
            ("Your model doesn't have the correct activations. The hidden `Dense` layers should be have `'relu'` activation, while the output layer should be linear (no activation).")
        try:
            input_shape = dense_layer.input_shape
        except:
            input_shape = None

class Q4(CodingProblem):
    _hint = ""
    _solution = ""
    _var = "model"
    def check(self, model):
        pass

class Q5(CodingProblem):
    pass

class Q6(ThoughtExperiment):
    pass


# Learning Rate and Batch Size
class Q7(ThoughtExperiment):
    pass


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3, Q4, Q5, Q6, Q7,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
