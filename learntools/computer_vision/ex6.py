import tensorflow as tf

from learntools.core import *


class Q1(ThoughtExperiment):
    _hint = """Remember that whatever transformation you apply should at the least preserve class distinctions. What are ways you could transform an image of a forest so that it still looked (more or less) like a forest?
"""
    _solution = """It seems to this author that flips and rotations would be worth trying first since there's no concept of orientation for pictures taken straight overhead. None of the transformations seem likely to confuse classes, however.
"""


class Q2(ThoughtExperiment):
    _hint = """Remember that whatever transformation you apply should at the least preserve class distinctions. What are ways you could transform an image of a rose so that it still looked (more or less) like a rose?
"""

    _solution = """It seems to this author that horizontal flips and moderate rotations would be worth trying first. Some augmentation libraries include transformations of hue (like red to blue). Since the color of a flower seems distinctive of its class, a change of hue might be less successful. On the other hand, there is suprising variety in cultivated flowers like roses, so, depending on the dataset, this might be an improvement after all!

"""


class Q3(CodingProblem):
    _var = "model"
    _hint = """
Your answer should look something like:

```python
model = keras.Sequential([
    layers.InputLayer(input_shape=[128, 128, 3]),
    
    # Data Augmentation
    preprocessing.____,
    preprocessing.____,
    preprocessing.____,
    
    # Block One
    layers.BatchNormalization(renorm=True),
    layers.Conv2D(filters=64, kernel_size=3, activation='relu', padding='same'),
    layers.MaxPool2D(),
    
    # More layers follow...
])
```

"""
    _solution = CS(
        """
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    layers.InputLayer(input_shape=[128, 128, 3]),
    
    # Data Augmentation
    preprocessing.RandomContrast(factor=0.10),
    preprocessing.RandomFlip(mode='horizontal'),
    preprocessing.RandomRotation(factor=0.10),
    
    # Block One
    layers.BatchNormalization(renorm=True),
    layers.Conv2D(filters=64, kernel_size=3, activation='relu', padding='same'),
    layers.MaxPool2D(),

    # Block Two
    layers.BatchNormalization(renorm=True),
    layers.Conv2D(filters=128, kernel_size=3, activation='relu', padding='same'),
    layers.MaxPool2D(),

    # Block Three
    layers.BatchNormalization(renorm=True),
    layers.Conv2D(filters=256, kernel_size=3, activation='relu', padding='same'),
    layers.Conv2D(filters=256, kernel_size=3, activation='relu', padding='same'),
    layers.MaxPool2D(),

    # Head
    layers.BatchNormalization(renorm=True),
    layers.Flatten(),
    layers.Dense(8, activation='relu'),
    layers.Dense(1, activation='sigmoid'),
])
"""
    )

    def check(self, model):
        # Check for correct number of layers
        num_layers = len(model.layers)
        assert num_layers == 17, (
            "Your model doesn't have the right number of layers."
            + "Did you add all three preprocessing layers?"
        )

        # Check for correct layer types
        layer_classes = [layer.__class__.__name__ for layer in model.layers]
        assert all(
            [
                layer_classes[0] == "RandomContrast",
                layer_classes[1] == "RandomFlip",
                layer_classes[2] == "RandomRotation",
            ]
        ), (
            "Your model doesn't have the right kind of preprocessing layers. "
            + "You should have `RandomContrast`, `RandomFlip`, and `RandomRotation`, "
            + "in that order, for the second, third, and fourth layers."
        )

        # Check for correct parameters
        contrast = model.layers[0].factor
        flip = model.layers[1].mode
        rotation = model.layers[2].factor
        assert (
            contrast == 0.1
        ), "Be sure to use a contrast factor of 0.1. You used {}.".format(
            contrast
        )
        assert (
            flip == "horizontal"
        ), "Be sure to use a `'horizaontal'` flip. You used `{}`.".format(flip)
        assert (
            rotation == 0.1
        ), "Be sure to use a rotation factor of 0.1. You used {}.".format(
            rotation
        )


class Q4(ThoughtExperiment):
    _solution = """
The learning curves in this model stayed close together for much longer than in previous models. This suggests that the augmentation helped prevent overfitting, allowing the model to continue improving.

And notice that this model achieved the highest accuracy of all the models in the course! This won't always be the case, but it shows that a well-designed custom convnet can sometimes perform as well or better than a much larger pretrained model. Depending on your application, having a smaller model (which requires fewer resources) could be a big advantage.
"""


qvars = bind_exercises(globals(), [Q1, Q2, Q3, Q4,], var_format="q_{n}",)
__all__ = list(qvars)
