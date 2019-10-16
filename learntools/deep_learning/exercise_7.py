import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from learntools.core import *
from tensorflow import keras

import tensorflow as tf

print("Using TensorFlow version {}".format(tf.__version__))
class StartSequentialModel(CodingProblem):
    _vars = ['fashion_model']

    def check(self, fashion_model):
        assert (type(fashion_model) == keras.models.Sequential), \
               ("Set fashion model to be a Sequential() model.")

    _solution = CS(
"""
fashion_model = Sequential()
"""
)

class AddFirstLayer(CodingProblem):
    _vars = ['fashion_model']

    def check(self, fashion_model):
        first_layer = fashion_model.layers[0]
        desired_input_shape = (None, 28, 28, 1)
        useful_text = "\nIt is hard to change a layer once you have added it. Recreate `fashion_model` and run `fashion_model` again after fixing this problem"
        assert (len(fashion_model.layers) == 1), \
               ("You should have 1 layer at this point but you have {}".format(len(fashion_model.layers)))
        assert (first_layer.input_shape == desired_input_shape), \
               ("First layer should have shape {} but instead it is {}. ".format(desired_input_shape, first_layer.input_shape) + useful_text)
        assert (first_layer.activation.__name__ == 'relu'), \
               ("You haven't set `relu` as the activation function. " + useful_text)
        assert (first_layer.kernel_size == (3, 3)), \
               ("The kernel size should be (3, 3) but yours is {}.".format(first_layer.kernel_size))
        assert (first_layer.filters == 12), \
               ("The first layer should have 12 filters but you have {}.".format(first_layer.filters))

    _hint = "The `input_shape` argument should be input_shape = (img_rows, img_cols, 1). " \
            "The other arguments you need are `units`, `kernel_size` and `"

    _solution = CS(
"""
fashion_model.add(Conv2D(12,
                         activation='relu',
                         kernel_size=3,
                         input_shape = (img_rows, img_cols, 1)))
"""
)

class AddMoreLayers(CodingProblem):
    _vars = ['fashion_model']

    def check(self, fashion_model):
        layers = fashion_model.layers
        last_layer = fashion_model.layers[-1]
        useful_text = "Use `fashion_model.summary()` to see your current model architecture."
        assert (len(layers) == 6), \
               ("You should have 6 layers, but actually have {}. ".format(useful_text) + useful_text)
        assert (type(fashion_model.layers[3]) == keras.layers.Flatten), \
               ("You should have a Flatten layer as the 4th layer. " + useful_text)
        assert (last_layer.activation.__name__ == 'softmax'), \
               ("Your last layer's activation function should be softmax"
                "but it is {}. Fix this in your code and rebuild the model by rerunning all model-building cells".format(last_layer.activation.__name__))
        assert (last_layer.output_shape == (None, 10)), \
               ("The number of nodes in your layer doesn't match the number of prediction categories. "
                "Last layer shape should be (None, 10) but it is ".format(last_layer.output_shape) + \
                ". Fix this in your code and re-run all model-building cells.")


    _solution = CS(
"""
fashion_model.add(Conv2D(20, activation='relu', kernel_size=3))
fashion_model.add(Conv2D(20, activation='relu', kernel_size=3))
fashion_model.add(Flatten())
fashion_model.add(Dense(100, activation='relu'))
fashion_model.add(Dense(10, activation='softmax'))
"""
)

class CompileModel(CodingProblem):
    _vars = ['fashion_model']

    def check(self, fashion_model):
        # TODO: Re-enable everything in this check after we are settled on TF 2.x
        # Ran into a bunch of problems here while API's were changing
        # assert (fashion_model.optimizer is not None), \
        #       ("You don't have an optimizer set. Did you run `fashion_model.compile` with an optimizer argument")

        # optimizer_name = fashion_model.optimizer._tf_api_names[0]
        # correct_optimizer_name = 'keras.optimizers.Adam'
        # assert(optimizer_name == correct_optimizer_name), \
        #       ("You didn't get the optimizer set correctly. It should be `adam`")
        # n_metrics = len(fashion_model.metrics)
        # assert (n_metrics == 1), \
        #       ("You should have a list with 1 item for the metric argument. You had {}".format(n_metrics))
        # metric = fashion_model.metrics[0]
        # First criterion is for older versions of tf. Second is for later versions
        # assert ((metric == 'accuracy') or (metric._name == 'acc')), \
        #       ("You need to set metrics=['accuracy']")
        pass
    _solution = CS(
"""
fashion_model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
"""
)

class FitFullDLModel(CodingProblem):
    _vars = ['fashion_model']

    def check(self, fashion_model):
        assert('history' in dir(fashion_model)), \
              ('You have not fit the model yet.')
        assert("val_loss" in fashion_model.history.history), \
              ('The way you fit the model did not generate validation scores. Specify `validation_split`')
    _solution = CS(
"""
fashion_model.fit(x, y, batch_size=100, epochs=4, validation_split=0.2)
"""
)

class CreateNewDLModelFromScratch(CodingProblem):
    _vars = ['second_fashion_model']

    def check(self, second_fashion_model):
        print("Model summary from second_fashion_model.summary()")
        print(second_fashion_model.summary())
        first_layer = second_fashion_model.layers[0]
        last_layer = second_fashion_model.layers[-1]

        desired_input_shape = (None, 28, 28, 1)
        assert (first_layer.input_shape == desired_input_shape), \
               ("First layer should have shape {} but instead it is {}. ".format(desired_input_shape, first_layer.input_shape) + useful_text)
        assert (len(second_fashion_model.layers) > 1), \
               ("Use more than 1 layer for a more accurate model.")
        assert (last_layer.output_shape == (None, 10)), \
               ("The number of nodes in your layer doesn't match the number of prediction categories.")
        assert (second_fashion_model.optimizer is not None), \
               ("You don't have an optimizer set. Did you run `second_fashion_model.compile`")
        assert('history' in dir(second_fashion_model)), \
              ('You have not fit the model yet.')
        assert("val_acc" in second_fashion_model.history.history), \
              ('The way you fit the model did not generate validation accuracy. Specify `validation_split` and compile with metrics=["accuracy"]')
        model_val_acc = second_fashion_model.history.history['val_acc'][-1]
        assert(model_val_acc > 0.75), \
              ('You have completed all the model building steps correctly, but your validation accuracy '
               'of {} can be improved. Try changing the model to see if you can get a better score'.format(model_val_acc))

    _hint = "Start by copying the code from `fashion_model` and then change layers as you choose. " + \
            "You'll develop intuition for what changes are worth making with practice. The next lesson " + \
            "gives a good strategy of building large model and using a special techniques to reduce overfitting."
    _solution = CS(
"""
second_fashion_model = Sequential()
second_fashion_model.add(Conv2D(12,
                         activation='relu',
                         kernel_size=3,
                         input_shape = (img_rows, img_cols, 1)))
# Changed kernel sizes to be 2
second_fashion_model.add(Conv2D(20, activation='relu', kernel_size=2))
second_fashion_model.add(Conv2D(20, activation='relu', kernel_size=2))
# added an addition Conv2D layer
second_fashion_model.add(Conv2D(20, activation='relu', kernel_size=2))
second_fashion_model.add(Flatten())
second_fashion_model.add(Dense(100, activation='relu'))
# It is important not to change the last layer. First argument matches number of classes. Softmax guarantees we get reasonable probabilities
second_fashion_model.add(Dense(10, activation='softmax'))

second_fashion_model.compile(loss='categorical_crossentropy',
                             optimizer='adam',
                             metrics=['accuracy'])

second_fashion_model.fit(x, y, batch_size=100, epochs=4, validation_split=0.2)
"""
)


qvars = bind_exercises(globals(), [
    StartSequentialModel,
    AddFirstLayer,
    AddMoreLayers,
    CompileModel,
    FitFullDLModel,
    CreateNewDLModelFromScratch,
    ],
    var_format='q_{n}',
    )

__all__ = list(qvars)
