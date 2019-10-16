import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from learntools.core import *

class WhyTwoGenerators(ThoughtExperiment):
    _solution = \
"""
We want to do data augmentation when fitting the model for the reasons mentioned
in the video (including a reduction in overfitting, by giving us more data to work with).

But we don't want to change how we test the model. So the validation generator
will use an ImageDataGenerator without augmentation. That allows a straightforward
comparison between different training procedures (e.g. training with augmentation
and without it).

If the augmentation made it harder to predict the label associated with an image
(e.g. because of how the image was cropped in augmentation) that would make it misleading
to compare scores to another procedure where the validation data was only original images.
"""


class RotationCriticism(ThoughtExperiment):
    _solution = \
"""
The goal in this problem is to tell if an image is upright or sideways.  Rotating images
moderately might cause images that don't feel cleanly in either category.

Since data augmentation affects images without touching the labels, a dramatic rotation
would mean some images are used for training with the wrong label (e.g. an image would be rotated
sideways by the generator, and still have a label of being upright)
"""

class CodeWithAugmentation(CodingProblem):
    _vars = ['my_new_model', 'train_generator', 'validation_generator',
             'data_generator_with_aug', 'data_generator_no_aug']

    _hint = "The first argument to fit_generator is the generator with the training data"
    _solution = CS(
"""
train_generator = data_generator_with_aug.flow_from_directory(
        directory = '../input/dogs-gone-sideways/train',
        target_size=(image_size, image_size),
        batch_size=12,
        class_mode='categorical')

# Specify which type of ImageDataGenerator above is to load in validation data
validation_generator = data_generator_no_aug.flow_from_directory(
        directory = '../input/dogs-gone-sideways/val',
        target_size=(image_size, image_size),
        class_mode='categorical')

my_new_model.fit_generator(
        train_generator,
        epochs = 3,
        steps_per_epoch=19,
        validation_data=validation_generator)
"""
)

    def check(self, my_new_model, train_generator, validation_generator, data_generator_with_aug, data_generator_no_aug):
        assert (train_generator.image_data_generator is data_generator_with_aug), \
               ("train_generator is using the wrong ImageDataGenerator")
        assert (validation_generator.image_data_generator is data_generator_no_aug), \
               ("validation_generator is using the wrong ImageDataGenerator")
        # TODO: Check they used the right validation generator. The following
        # check worked in previous versions of TF but then broke.
        # assert (my_new_model.history.validation_data is validation_generator), \
        #       ("You have the wrong validation generator")


class DidAugmentationHelp(ThoughtExperiment):
    _solution = \
"""
Create `train_generator` usng `data_generator_no_aug` but don't
change other arguments to `train_generator`.

Run the model and see the resuling accuracy. Compare this to
the accuracy you got when `train_generator` used augmentation.

Our validation dataset is very small, so there's a little bit
of luck or randomness in the exact score from any
model run. Validation scores will be more reliable as you
start using larger datasets.
"""


qvars = bind_exercises(globals(), [
    WhyTwoGenerators,
    RotationCriticism,
    CodeWithAugmentation,
    DidAugmentationHelp
    ],
    var_format='q_{n}',
    )

__all__ = list(qvars)
