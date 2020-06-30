from learntools.core import *

class Q1(EqualityCheckProblem):
    _var = 'pretrained_base.trainable'
    _expected = False
    _hint = """ When doing transfer learning, it's generally not a good idea to retrain the entire base -- at least not without some care. The reason is that the random weights in the head will initially create large gradient updates, which propogate back into the base layers and destroy much of the pretraining. Using techniques known as **fine tuning** it's possible to further train the base on new data, but this requires some care to do well.
"""
    _solution = CS('pretrained_base.trainable = False')


class Q2(CodingProblem):
    _var = 'model'
    _hint = "You need to add two new `Dense` layers. Everything in `Sequential` should end up the same as in the tutorial."
    _solution = CS(""" 
import tensorflow.keras as keras
import tensorflow.keras.layers as layers

model = Sequential([
    pretrained_base,
    layers.Flatten(),
    layers.Dense(8, activation='relu'),
    layers.Dense(1, activation='sigmoid'),
])
""")
    def check(self, model):
        layer_classes = [layer.__class__.__name__ for layer in model.layers]
        assert (len(model.layers) == 4,
                "You should have four lines inside of `Sequential`. You had {}.".format(len(model.layers)))
        assert (layer_classes[2] == 'Dense' and layer_classes[3] == 'Dense',
                "The two layers you add should both be `Dense` layers. You added a {} layer and a {} layer.".format(layer_classes[2], layer_classes[3]))
        # assert ( , ) # TODO: parameter check

# TODO: change to coding problem
class Q3(EqualityCheckProblem):
    _vars = ['loss', 'accuracy']
    _expected = ['binary_crossentropy', 'binary_accuracy']
    _hint = "These are the same as in the tutorial."
    _solution = CS("""
loss = 'binary_crossentropy'
accuracy = 'binary_accuracy'
""")


class Q4(ThoughtExperiment):
    _solution = """ That the training loss and validation loss stay fairly close is evidence that the model isn't just memorizing the training data, but rather learning general properties of the two classes. But, because this model converges at a loss greater than the VGG16 model, it's likely that it is underfitting some, and could benefit from some extra capacity.
"""
