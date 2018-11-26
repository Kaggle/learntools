import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from learntools.core.utils import bind_exercises
from learntools.core.richtext import CodeSolution as CS
from learntools.core.problem import *


class SetTraininableAndNumClasses(CodingProblem):
    _vars = ['num_classes', 'my_new_model']
    _hint = \
"""num_classes is the number of categories your model chooses between for each prediction.
Think about the problem to determine the answer. " + my_new_model[0].layers.trainable is
set to either True or False"""

    _solution = CS(
"""
num_classes = 2
resnet_weights_path = '../input/resnet50/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5'

my_new_model = Sequential()
my_new_model.add(ResNet50(include_top=False, pooling='avg', weights=resnet_weights_path))
my_new_model.add(Dense(num_classes, activation='softmax'))

# Indicate whether the first layer should be trained/changed or not.
my_new_model.layers[0].trainable = False
"""
)

    def check(self, num_classes, my_new_model):
        assert (num_classes == 2), ("num_classes should be 2.  You set it to %d".format(num_classes))
        assert (not my_new_model.layers[0].trainable), \
        ("Layer 0 of your model should not be trainable. It was trained on another dataset, and will be hard to improve.")

class CompileTransferLearningModel(CodingProblem):
    _vars = ['my_new_model']
    def check(self, my_new_model):
        assert ('loss' in dir(my_new_model)), ("You have not compiled your model yet")

    _soluiton = CS("my_new_model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])")

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
    _vars = ['fit_stats']
    _hint = "To get steps_per_epoch, divide the number of images by the batch size."
    def check(self, fit_stats):
        their_val_dir = fit_stats.validation_data.directory
        their_val_loss = fit_stats.history['val_loss']
        their_num_steps = b.params['steps']
        assert (their_val_dir == '../input/dogs-gone-sideways/val'),\
               ("The validation directory should be `../input/dogs-gone-sideways/val`. Yours was {}".format(their_val_dir))
        assert (their_num_steps == 22), ("Should have 22 steps per epoch. You had {}".format(their_num_steps))
        assert (their_val_loss < 0.4), \
                ("Your validation loss is {}. It should be around 0.34. Something isn't right".format(their_val_loss))


qvars = bind_exercises(globals(), [
    SetTraininableAndNumClasses,
    CompileTransferLearningModel,
    WhatCompileArgsAffectModel,
    FitTransferModel,
    ],
    tutorial_id=76,
    var_format='step_{n}',
    )

__all__ = list(qvars)
