from learntools.core import *

class Q1(CodingProblem):
    _var = 'pretrained_base'
    _hint = """ When doing transfer learning, it's generally not a good idea to retrain the entire base -- at least not without some care. The reason is that the random weights in the head will initially create large gradient updates, which propogate back into the base layers and destroy much of the pretraining. Using techniques known as **fine tuning** it's possible to further train the base on new data, but this requires some care to do well.
"""
    _solution = CS('pretrained_base.trainable = False')
    def check(self, pretrained_base):
        assert (not pretrained_base.trainable)

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


class Q3(CodingProblem):
    _hint = "This is a *binary* classification problem."
    _solution = CS("""
model.compile(
    optimizer='adam',
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


class Q4(ThoughtExperiment):
    _solution = """ That the training loss and validation loss stay fairly close is evidence that the model isn't just memorizing the training data, but rather learning general properties of the two classes. But, because this model converges at a loss greater than the VGG16 model, it's likely that it is underfitting some, and could benefit from some extra capacity.
"""

    
qvars = bind_exercises(
    globals(),
    [Q1, Q2, Q3, Q4],
    var_format='q_{n}',
)

__all__ = list(qvars)
