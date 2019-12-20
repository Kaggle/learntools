import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from learntools.core import *

class AddStrides(CodingProblem):
    _vars = ['fashion_model_1']

    def check(self, fashion_model_1):
        assert (fashion_model_1.layers[1].strides == (2, 2)), \
               ("You haven't set the second convolutional layer's stride correctly")

    _solution = CS(
"""
fashion_model_1 = Sequential()
fashion_model_1.add(Conv2D(16, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(img_rows, img_cols, 1)))
# This is the only line that changed
fashion_model_1.add(Conv2D(16, (3, 3), activation='relu', strides=2))
fashion_model_1.add(Flatten())
fashion_model_1.add(Dense(128, activation='relu'))
fashion_model_1.add(Dense(num_classes, activation='softmax'))

# the fit and compile steps are not shown here since they did not change
"""
)


qvars = bind_exercises(globals(), [
    AddStrides,
    ],
    var_format='q_{n}',
    )

__all__ = list(qvars)
