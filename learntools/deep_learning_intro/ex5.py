from learntools.core import *


# Add Dropout
class Q1(CodingProblem):
    _hint = """Your answer should look something like:
```python
model = keras.Sequential([
    # Dense
    # Dropout
    # Dense
    # Droput
    # Dense
])
```
"""
    _solution = CS("""
model = keras.Sequential([
    layers.Dense(128, activation='relu', input_shape=input_shape),
    layers.Dropout(0.3),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(1)
])
""")
    _var = "model"
    def check(self, model):
        dense_layer = model.layers[0]
        layer_classes = [layer.__class__.__name__ for layer in model.layers]
        true_classes = ['Dense', 'Dropout', 'Dense', 'Dropout', 'Dense']
        # Check layer class
        assert (layer_classes == true_classes), \
            ("Your model doesn't have the correct kinds of layers. You should have five layers with classes: {}.".format(true_classes))
        # Check activation functions
        dense_activations = [layer.activation.__name__
                             for layer in model.layers
                             if layer.__class__.__name__ is 'Dense']
        true_activations = ['relu', 'relu', 'linear']
        assert (dense_activations == true_activations), \
            ("Your model doesn't have the correct activations. The hidden `Dense` layers should be have `'relu'` activation, while the output layer should be linear (no activation).")
        # Check number of units
        dense_units = [layer.units
                       for layer in model.layers
                       if layer.__class__.__name__ is 'Dense']
        true_units = [128, 64, 1]
        assert (dense_units == true_units), \
            ("Your model doesn't have the correct number of units. The units of the `Dense` layers should be {}.".format(true_units))
        # Check dropout rates
        dropout_rates = [layer.rate
                         for layer in model.layers
                         if layer.__class__.__name__ is 'Dropout']
        true_rates = [0.3, 0.3]
        assert (dropout_rates == true_rates), \
            ("Your model doesn't have the correct dropout rates. The rates of the `Dropout` layers should be {}.".format(true_rates))


# Evaluate Dropout
class Q2(ThoughtExperiment):
    _solution = """
From the learning curves, you can see that the validation loss remains near a constant minimum even though the training loss continues to decrease. So we can see that adding dropout did prevent overfitting this time. Moreover, by making it harder for the network to fit spurious patterns, dropout may have encouraged the network to seek out more of the true patterns, possibly improving the validation loss some as well).
"""


# Add BatchNormalization
class Q3(CodingProblem):
    _hint = """Your answer should look something like:
```python
model = keras.Sequential([
    # Batch Normalization
    # Dense
    # Batch Normalization
    # Dense
    # Batch Normalization
    # Dense
    # Batch Normalization
    # Dense
])
```
"""
    _solution = CS("""
model = keras.Sequential([
    layers.BatchNormalization(input_shape=input_shape),
    layers.Dense(512, activation='relu'),
    layers.BatchNormalization(),
    layers.Dense(512, activation='relu'),
    layers.BatchNormalization(),
    layers.Dense(512, activation='relu'),
    layers.BatchNormalization(),
    layers.Dense(1),
])
""")
    _var = "model"
    def check(self, model):
        dense_layer = model.layers[0]
        layer_classes = [layer.__class__.__name__ for layer in model.layers]
        true_classes = ['BatchNormalization', 'Dense',
                        'BatchNormalization', 'Dense',
                        'BatchNormalization', 'Dense',
                        'BatchNormalization', 'Dense',]
        # Check layer class
        assert (layer_classes == true_classes), \
            ("Your model doesn't have the correct kinds of layers. You should have eight layers with classes: {}.".format(true_classes))
        # Check activation functions
        dense_activations = [layer.activation.__name__
                             for layer in model.layers
                             if layer.__class__.__name__ is 'Dense']
        true_activations = ['relu', 'relu', 'relu', 'linear']
        assert (dense_activations == true_activations), \
            ("Your model doesn't have the correct activations. The hidden `Dense` layers should be have `'relu'` activation, while the output layer should be linear (no activation).")
        # Check number of units
        dense_units = [layer.units
                       for layer in model.layers
                       if layer.__class__.__name__ is 'Dense']
        true_units = [512, 512, 512, 1]
        assert (dense_units == true_units), \
            ("Your model doesn't have the correct number of units. The units of the `Dense` layers should be {}.".format(true_units))


# Evaluate BatchNormalization
class Q4(ThoughtExperiment):
    _solution = """
You can see that adding batch normalization was a big improvement on the first attempt! By adaptively scaling the data as it passes through the network, batch normalization can let you train models on difficult datasets.
"""


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3, Q4,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)

