import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from learntools.core import *


class SetTraininableAndNumClasses(CodingProblem):
    _vars = ['num_classes', 'my_new_model']
    _hint = \
"""num_classes is the number of categories your model chooses between for each prediction.
Think about the problem to determine the answer. " + my_new_model[0].layers.trainable is
set to either True or False"""

    _solution = CS(
"""
num_classes = 2    # First line that was changed
resnet_weights_path = '../input/resnet50/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5'

my_new_model = Sequential()
my_new_model.add(ResNet50(include_top=False, pooling='avg', weights=resnet_weights_path))
my_new_model.add(Dense(num_classes, activation='softmax'))

# Indicate whether the first layer should be trained/changed or not.
my_new_model.layers[0].trainable = False   # Other line that was changed
"""
)

    def check(self, num_classes, my_new_model):
        assert (num_classes == 2), ("num_classes should be 2.  You set it to %d".format(num_classes))
        assert (not my_new_model.layers[0].trainable), \
        ("Layer 0 of your model should not be trainable. It was trained on another dataset, and will be hard to improve.")

class CompileTransferLearningModel(ThoughtExperiment):
    _solution = \
"""
The compile model doesn't change the values in any convolutions.  In fact, your model has not even
received an argument with data yet.  Compile specifies how your model will make updates a later
`fit` step where it receives data.  That is the part that will take longer.
"""

class WhatCompileArgsAffectModel(ThoughtExperiment):
    _solution = \
    """
- **optimizer** determines how we determine the numerical values that make up the model. So it can affect the resulting model and predictions
- **loss** determines what goal we optimize when determining numerical values in the model. So it can affect the resulting model and predictions
- **metrics** determines only what we print out while the model is being built, but it doesn't affect the model itself.

You may not understand all of this yet. That's totally fine for now.  It will become
clearer in an upcoming lesson (called A Deeper Understanding of Deep Learning).
"""

class FitTransferModel(CodingProblem):
    _vars = ['fit_stats', 'validation_generator']
    _hint = "To get steps_per_epoch, divide the number of images by the batch size."
    def check(self, fit_stats, validation_generator):
        their_val_dir = validation_generator.directory
        their_val_loss = fit_stats.history['val_loss'][0]
        their_num_steps = fit_stats.params['steps']
        correct_val_dir = '../input/dogs-gone-sideways/images/val'
        assert (their_val_dir == correct_val_dir),\
               ("The validation directory should be `{}`. Yours was `{}`".format(correct_val_dir, their_val_dir))
        assert (their_num_steps == 22), ("Should have 22 steps per epoch. You had {}".format(their_num_steps))
    _solution = CS(
"""
image_size = 224
data_generator = ImageDataGenerator(preprocess_input)

train_generator = data_generator.flow_from_directory(
                                        directory="../input/dogs-gone-sideways/images/train",
                                        target_size=(image_size, image_size),
                                        batch_size=10,
                                        class_mode='categorical')

validation_generator = data_generator.flow_from_directory(
                                        directory="../input/dogs-gone-sideways/images/val",
                                        target_size=(image_size, image_size),
                                        class_mode='categorical')

# fit_stats below saves some statistics describing how model fitting went
# the key role of the following line is how it changes my_new_model by fitting to data
fit_stats = my_new_model.fit_generator(train_generator,
                                       steps_per_epoch=22,
                                       validation_data=validation_generator,
                                       validation_steps=1)
"""
    )

qvars = bind_exercises(globals(), [
    SetTraininableAndNumClasses,
    CompileTransferLearningModel,
    WhatCompileArgsAffectModel,
    FitTransferModel,
    ],
    var_format='step_{n}',
    )

__all__ = list(qvars)
