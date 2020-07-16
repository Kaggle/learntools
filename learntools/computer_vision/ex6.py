from learntools.core import *
import tensorflow as tf


# Free
class Q1(CodingProblem):
    _solution = ""
    _hint = ""
    def check(self):
        pass


class Q2A(ThoughtExperiment):
    _hint = """Remember that whatever transformation you apply should at the least preserve class distinctions. What are ways you could transform an image of a forest so that it still looked (more or less) like a forest?
"""
    _solution = """It seems to this author that flips and rotations would be worth trying first since there's no concept of orientation for pictures taken straight overhead. None of the transformations seem likely to confuse classes, however.
"""

class Q2B(ThoughtExperiment):
    _hint = """Remember that whatever transformation you apply should at the least preserve class distinctions. What are ways you could transform an image of a rose so that it still looked (more or less) like a rose?
"""

    _solution = """It seems to this author that horizontal flips and moderate rotations would be worth trying first. Some augmentation libraries include transformations of hue (like red to blue). Since the color of a flower seems distinctive of its class, a change of hue might be less successful. On the other hand, there is suprising variety in cultivated flowers like roses, so, depending on the dataset, this might be an improvement after all!

"""

Q2 = MultipartProblem(Q2A, Q2B)


class Q3A(CodingProblem):
    _var = 'model'
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
    layers.Conv2D(filters=64, kernel_size=3, activation='relu', padding='same'),
    layers.MaxPool2D(),
    
    # More layers follow...
])
```

"""
    _solution = CS("""
#%%RM_IF(PROD)%%
import tensorflow.keras as keras
import tensorflow.keras.layers as layers

model = keras.Sequential([
    layers.InputLayer(input_shape=[128, 128, 3]),
    
    # Data Augmentation
    preprocessing.RandomContrast(factor=0.10),
    preprocessing.RandomFlip(mode='horizontal'),
    preprocessing.RandomRotation(factor=0.10),
    
    # Block One
    layers.Conv2D(filters=64, kernel_size=3, activation='relu', padding='same'),
    layers.MaxPool2D(),

    # Block Two
    layers.Conv2D(filters=128, kernel_size=3, activation='relu', padding='same'),
    layers.Conv2D(filters=128, kernel_size=3, activation='relu', padding='same'),
    layers.MaxPool2D(),

    # Block Three
    layers.Conv2D(filters=256, kernel_size=3, activation='relu', padding='same'),
    layers.Conv2D(filters=256, kernel_size=3, activation='relu', padding='same'),
    layers.Conv2D(filters=256, kernel_size=3, activation='relu', padding='same'),
    layers.MaxPool2D(),

    # Head
    layers.Flatten(),
    layers.Dense(8, activation='relu'),
    layers.Dense(1, activation='sigmoid'),
])
q_3.a.assert_check_passed()
""")

    def check(self, model):
        # Check for correct number of layers
        num_layers = len(model.layers)
        assert num_layers == 1, \
            ("Your model should have 1 layers, but your model has {}. " +
             "Did you add all three preprocessing layers?")

        # Check for correct layer types
        layer_classes = [layer.__class__.__name__ for layer in model.layers]
        assert all([
            layer_classes[1] == 'RandomContrast',
            layer_classes[2] == 'RandomFlip',
            layer_classes[3] == 'RandomRotation',
        ]), \
        ("Your model doesn't have the right kind of preprocessing layers. " +
         "You should have `RandomContrast`, `RandomFlip`, and `RandomRotation`, " +
         "in that order, for the second, third, and fourth layers.")

        # Check for correct parameters
        contrast = model.layers[1]
        flip = model.layers[2]
        rotation = model.layers[3]
        assert contrast, \
            ""
        assert flip, \
            ""
        assert rotation, \
            ""
        

class Q3B(ThoughtExperiment):
    _solution = """


"""

Q3 = MultipartProblem(Q3A, Q3B)    

qvars = bind_exercises(globals(), [
        Q1, Q2, Q3,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
