from learntools.core import *

# Define Model
class Q1(CodingProblem):
    _hint = """Your answer should look something like:
```python
model = keras.Sequential([
    # Batch Normalization

    # Dense
    # Batch Normalization
    # Dropout

    # Dense
    # Batch Normalization
    # Dropout

    # Dense
])
```
"""
    _solution = CS("""
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    layers.BatchNormalization(input_shape=input_shape),
    layers.Dense(256, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    layers.Dense(256, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    layers.Dense(1, activation='sigmoid'),
])
q_1.assert_check_passed()
""")
    _var = "model"
    def check(self, model):
        dense_layer = model.layers[0]
        layer_classes = [layer.__class__.__name__ for layer in model.layers]
        true_classes = ['BatchNormalization',
                        'Dense', 'BatchNormalization', 'Dropout',
                        'Dense', 'BatchNormalization', 'Dropout',
                        'Dense']
        # Check layer class
        assert (layer_classes == true_classes), \
            ("Your model doesn't have the correct kinds of layers. You should have layers with classes: {}.".format(true_classes))
        # Check activation functions
        dense_activations = [layer.activation.__name__
                             for layer in model.layers
                             if layer.__class__.__name__ is 'Dense']
        true_activations = ['relu', 'relu', 'sigmoid']
        assert (dense_activations == true_activations), \
            ("Your model doesn't have the correct activations. The hidden `Dense` layers should be have `'relu'` activation, while the output layer should be sigmoid.")
        # Check number of units
        dense_units = [layer.units
                       for layer in model.layers
                       if layer.__class__.__name__ is 'Dense']
        true_units = [256, 256, 1]
        assert (dense_units == true_units), \
            ("Your model doesn't have the correct number of units. The units of the `Dense` layers should be {}.".format(true_units))


# Compile
class Q2(CodingProblem):
    _hint = """Your code should look something like:
```python
model.compile(
optimizer=____,
loss=____,
metrics=____,
)
```
"""
    _solution = CS("""
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['binary_accuracy'],
)
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
        try:
            metrics = model.compiled_metrics._metrics
        except:
            metrics = None            
        assert (optimizer is not None and loss is not None and metrics is not None), \
        ("You are missing the loss, the optimizer, or the metrics.")
        true_loss = 'binary_crossentropy'
        assert (loss.lower() == true_loss), \
            ("The loss should be `'{}'`. You gave `'{}'`".format(true_loss, loss))
        true_opt = 'adam'
        assert (optimizer.lower() == true_opt), \
            ("The optimizer should be `'{}'`. You gave `{}`".format(true_opt, optimizer))
        true_metrics = ['binary_accuracy']
        assert (metrics[0].lower() == true_metrics[0].lower()), \
            ("The metrics should be `{}`. You gave `{}`.".format(true_metrics, metrics))
        

# Evaluate
class Q3(ThoughtExperiment):
    _solution = "Though we can see the training loss continuing to fall, the early stopping callback prevented any overfitting. Moreover, the accuracy rose at the same rate as the cross-entropy fell, so it appears that minimizing cross-entropy was a good stand-in. All in all, it looks like this training was a success!"


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
