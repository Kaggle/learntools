from learntools.core import *
import tensorflow as tf


class Q1(CodingProblem):
    _hint = """You should add two `Conv2D` layers and then a `MaxPool2D` layer. They will be just the same as the other layers in the model, except for some of the parameter values."""
    _solution = CS("""
import tensorflow.keras as keras
import tensorflow.keras.layers as layers

model = keras.Sequential([
    # Block One
    layers.Conv2D(filters=64, kernel_size=5, activation='relu', padding='same',
                  input_shape=[192, 192, 3]),
    layers.MaxPool2D(),

    # Block Two
    layers.Conv2D(filters=256, kernel_size=3, activation='relu', padding='same'),
    layers.Conv2D(filters=256, kernel_size=3, activation='relu', padding='same'),
    layers.MaxPool2D(),

    # Block Three
    layers.Conv2D(filters=512, kernel_size=3, activation='relu', padding='same'),
    layers.Conv2D(filters=512, kernel_size=3, activation='relu', padding='same'),
    layers.Conv2D(filters=512, kernel_size=3, activation='relu', padding='same'),
    layers.MaxPool2D(),

    # Head
    layers.Flatten(),
    layers.Dense(6, activation='relu'),
    layers.Dense(1, activation='sigmoid'),
])
""")
    _var = "model"
    
    def check(self, model):
        # Check for correct number of layers
        num_layers = len(model.layers)
        assert((num_layers == 12),
               ("Your model should have 12 layers, but your model has {}."
                .format(num_layers)))
        
        # Check for correct layer types
        layer_classes = [layer.__class__.__name__ for layer in model.layers]
        assert((all([
            layer_classes[2] == 'Conv2D',
            layer_classes[3] == 'Conv2D',
            layer_classes[4] == 'MaxPooling2D',
        ])),
               ("Your model doesn't have the right kind of layers. " +
                "For the second block, you should have two convolutional layers " +
                "and then a maximum pooling layer."))

        # Check kernel size
        kernel_sizes = [model.layers[2].kernel_size,
                        model.layers[3].kernel_size]
        assert((kernel_sizes[0] == (3, 3) and kernel_sizes[1] == (3, 3)),
               ("Your convolutional layers don't have the right kernel size. " +
                "You should have `kernel_size=3` or `kernel_size=(3, 3) for both." +
                "Your model has {} for the first and {} for the second."
                .format(kernel_sizes[0], kernel_sizes[1])
                ))

        # Check filters
        filters = [model.layers[2].filters,
                   model.layers[3].filters]
        assert((filters[0] == 256 and filters[1] == 256),
               ("Your convolutional layers don't have the right number of filters." +
                "You should have 256 for both. Your model has {} for the first " +
                "and {} for the second."
                .format(filters[0], filters[1])
               ))

        # Check activations
        activations = [model.layers[2].activation.__name__,
                       model.layers[3].activation.__name__]
        assert((activations[0] is 'relu' and activations[1] is 'relu'),
               ("Your convolutional layers should both have `'relu'` activation."
               ))
        
        
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
        assert((loss == 'binary_crossentropy'),
               ("The loss should be `'binary_crossentropy'`. " +
                "You gave {}".format(loss)))

        metric = model.compiled_metrics._metrics
        assert((metric == 'binary_accuracy'),
               ("The metrics should be `['binary_accuracy']`. " +
                "You gave {}".format(metric)))


class Q3(ThoughtExperiment):
    pass


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
