from learntools.core import *

inputs = 50

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
""".format(inputs=inputs))

    def check(self, input_shape):
        assert (type(input_shape) in [list, tuple]), \
            ("""The input shape should be a list (or tuple) with a single integer, like `[__]`.""")
        assert (input_shape[0] not in [13, 14]), \
            ("Look at the columns of `X_train` for the number of input features, since `X_train` (the processed data) is what is actually being used as input.")
        assert (len(input_shape) == 1), \
            ("""You should use a list of length 1 here. Each entry in the `input_shape` list says how many input values you have in that dimension. The inputs here are numbers (one dimensional) and so your answer should look something like:
```python
input_shape = [____]
```
""")
        assert (input_shape[0] == inputs), \
            ("The number of inputs should be {good_inputs}, but you gave {bad_inputs}".format(good_inputs=inputs, bad_inputs=input_shape[0]))


# Model for Fuel Economy Prediction
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
""".format(inputs))
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
            ("Your model doesn't have the correct kinds of layers. You should have four layers with classes: Dense, Dense, Dense, Dense.")
        # Check input shape
        try:
            input_shape = dense_layer.input_shape
        except:
            input_shape = None
        assert (input_shape == (None, inputs)), \
            ("Your model should have {} inputs.".format(inputs))
        # Check activation functions
        dense_activations = [layer.activation.__name__ for layer in model.layers]
        true_activations = ['relu', 'relu', 'relu', 'linear']
        assert (dense_activations == true_activations), \
            ("Your model doesn't have the correct activations. The hidden `Dense` layers should be have `'relu'` activation, while the output layer should be linear (no activation).")

        # Check number of units
        layer_units = [layer.units for layer in model.layers]
        true_units = [64, 64, 64, 1]
        assert (layer_units == true_units), \
            ("Your model doesn't have the correct number of units. The units of the `Dense` layers should be 64, 64, 64, and 1, in that order.")

# Compile
class Q4(CodingProblem):
    _hint = """Your code should look something like:
```python
model.compile(
____,
____,
)
```
"""
    _solution = CS("""
model.compile(
    optimizer='adam',
    loss='mae'
)
q_4.assert_check_passed()
""")
    _var = "model"
    def check(self, model):
        try:
            optimizer = model.optimizer.__class__.__name__
        except:
            optimizer = None
        try:
            loss = model.compiled_loss._losses
        except:
            loss = None
        assert (optimizer is not None and loss is not None), \
        ("You are missing the loss or the optimizer.")
        assert (loss.lower() == 'mae'), \
            ("The loss should be `'mae'`. You gave `{}`".format(loss))
        assert (optimizer.lower() == 'adam'), \
            ("The optimizer should be `'adam'`. You gave `{}`".format(optimizer))


# Train the model
class Q5(CodingProblem):
    _hint = ""
    _solution = ""
    _var = "history"
    def check(self, history):
        # Epochs
        epochs = history.params['epochs']
        true_epochs = 100
        assert (epochs == true_epochs), \
            ("You have the incorrect number of epochs. You gave {}, but there should be {}.".format(epochs, true_epochs))
        # Batch Size
        # (examples * batch_percent) // epochs
        batch_size = (1107 * 0.75) // true_epochs
        true_batch_size = 128
        assert (batch_size == 8.0), \
            ("You have the incorrect number of batches. You gave {}, but there should be {}".format(batch_size, true_batch_size))
        # Validation Data
        assert ('val_loss' in history.history.keys()), \
            ("You need to include the validation data. Use the argument `validation_data=(X_train, y_train)`")


# Evaluate training
class Q6(ThoughtExperiment):
    _solution = "Most likely not. Once the learning curves level off, there won't usually be any advantage to training for additional epochs."

# Learning rate and batch size
class Q7(CodingProblem):
    _hint = ""
    _solution = ""
    def check(self):
        pass


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3, Q4, Q5, Q6, Q7,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
