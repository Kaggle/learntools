import tensorflow as tf

from learntools.core import *


class Q1(CodingProblem):
    _hint = """You should add two `Conv2D` layers and then a `MaxPool2D` layer. They will be just the same as the other layers in the model, except for some of the parameter values."""
    _solution = CS("""
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    # Block One
    layers.Conv2D(filters=32, kernel_size=3, activation='relu', padding='same',
                  input_shape=[128, 128, 3]),
    layers.MaxPool2D(),

    # Block Two
    layers.Conv2D(filters=64, kernel_size=3, activation='relu', padding='same'),
    layers.MaxPool2D(),

    # Block Three
    layers.Conv2D(filters=128, kernel_size=3, activation='relu', padding='same'),
    layers.Conv2D(filters=128, kernel_size=3, activation='relu', padding='same'),
    layers.MaxPool2D(),

    # Head
    layers.Flatten(),
    layers.Dense(6, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(1, activation='sigmoid'),
])
""")
    _var = "model"
    
    def check(self, model):
        # Check for correct number of layers
        num_layers = len(model.layers)
        assert num_layers == 11, \
("""You've added an incorrect number of layers. For `# Block Three`, try something like:

```python
layers.Conv2D(____),
layers.Conv2D(____),
layers.MaxPool2D(),
```
""")

        # Check for correct layer types
        layer_classes = [layer.__class__.__name__ for layer in model.layers]
        assert all([
            layer_classes[4] == 'Conv2D',
            layer_classes[5] == 'Conv2D',
            layer_classes[6] == 'MaxPooling2D',
        ]), \
        ("Your model doesn't have the right kind of layers. " +
         "For the second block, you should have two convolutional layers " +
         "and then a maximum pooling layer.")

        # Check kernel size
        kernel_sizes = [model.layers[4].kernel_size,
                        model.layers[5].kernel_size]
        assert (kernel_sizes[0] == (3, 3) and kernel_sizes[1] == (3, 3)), \
            (("Your convolutional layers don't have the right kernel size. " +
              "You should have `kernel_size=3` or `kernel_size=(3, 3) for both." +
              "Your model has {} for the first and {} for the second.")
             .format(kernel_sizes[0], kernel_sizes[1]))

        # Check filters
        filters = [model.layers[4].filters,
                   model.layers[5].filters]
        assert (filters[0] == 128 and filters[1] == 128), \
            (("Your convolutional layers don't have the right number of filters." +
              "You should have 128 for both. Your model has {} for the first " +
              "and {} for the second.")
             .format(filters[0], filters[1]))

        # Check activations
        activations = [model.layers[4].activation.__name__,
                       model.layers[5].activation.__name__]
        assert (activations[0] is 'relu' and activations[1] is 'relu'), \
            ("Your convolutional layers should both have `'relu'` activation.")

        
class Q2(CodingProblem):
    _hint = "This is a *binary* classification problem."
    _solution = CS("""
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss='binary_crossentropy',
    metrics=['binary_accuracy'],
)
""")
    _var = "model"
    def check(self, model):
        loss = model.compiled_loss._losses
        assert (loss == 'binary_crossentropy'), \
            (("The loss should be `'binary_crossentropy'`. " +
              "You gave {}")
             .format(loss))

        metric = model.compiled_metrics._metrics
        assert (metric == ['binary_accuracy']), \
            ("The metrics should be `['binary_accuracy']`. " +
             "You gave {}").format(metric)


class Q3(ThoughtExperiment):
    _solution = """
The learning curves for the model from the tutorial diverged fairly rapidly. This would indicate that it was prone to overfitting and in need of some regularization. The additional layer in our new model would make it even more prone to overfitting. However, adding some regularization with the `Dropout` layer helped prevent this. These changes improved the validation accuracy of the model by several points.
"""


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
