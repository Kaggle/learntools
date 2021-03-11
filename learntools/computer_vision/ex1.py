from learntools.core import *


class Q1(CodingProblem):
    _var = 'pretrained_base'
    _hint = "`True` or `False`?"
    _correct_message = """When doing transfer learning, it's generally not a good idea to retrain the entire base -- at least not without some care. The reason is that the random weights in the head will initially create large gradient updates, which propogate back into the base layers and destroy much of the pretraining. Using techniques known as **fine tuning** it's possible to further train the base on new data, but this requires some care to do well."""
    _solution = CS('pretrained_base.trainable = False')
    def check(self, pretrained_base):
        assert (not pretrained_base.trainable), \
               ("""The base should not be trainable. Since it's already been pretrained on a large dataset, you can expect that it will be hard to improve.""")


class Q2(CodingProblem):
    hidden_units = 6
    _var = 'model'
    _hint = "You need to add two new `Dense` layers. The first should have {} units and `'relu'` activation. The second should have 1 unit and `'sigmoid'` activation.".format(hidden_units)
    _solution = CS(""" 
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    pretrained_base,
    layers.Flatten(),
    layers.Dense({}, activation='relu'),
    layers.Dense(1, activation='sigmoid'),
])
""".format(hidden_units))

    def check(self, model):
        hidden_units = 6
        assert (len(model.layers) == 4), \
               ("""
You've added an incorrect number of layers. Try something like:
```python
model = Sequential([
    pretrained_base,
    layers.Flatten(),
    layers.Dense(____),
    layers.Dense(____),
])
```
""")

        layer_classes = [layer.__class__.__name__ for layer in model.layers]
        assert (layer_classes[2] == 'Dense' and layer_classes[3] == 'Dense'), \
               (("The two layers you add should both be `Dense` layers. " +
                 "You added a `{}` layer and a `{}` layer.")
                .format(layer_classes[2], layer_classes[3]))

        dense_1 = model.layers[-2]
        assert (dense_1.units == hidden_units and
                dense_1.activation.__name__ == 'relu'), \
                (("The first dense layer should have {} units with `{}` activation. " +
                  "Yours had {} units and `{}` activation.")
                 .format(hidden_units, 'relu',
                         dense_1.units, dense_1.activation.__name__))
        
        dense_2 = model.layers[-1]
        assert (dense_2.units == 1 and
                dense_2.activation.__name__ == 'sigmoid'), \
                (("The second dense layer should have {} units with `{}` activation. " +
                  "Yours had {} units and `{}` activation.")
                 .format(1, 'sigmoid',
                         dense_2.units, dense_2.activation.__name__))



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
        assert (loss == 'binary_crossentropy'), \
            (("The loss should be `'binary_crossentropy'`. " +
              "You gave `{}`").format(loss))

        metrics = model.compiled_metrics._metrics
        assert (metrics == ['binary_accuracy']), \
            (("The metrics should be `['binary_accuracy']`. " +
              "You gave `{}`").format(metrics))


class Q4(ThoughtExperiment):
    _solution = """That the training loss and validation loss stay fairly close is evidence that the model isn't just memorizing the training data, but rather learning general properties of the two classes. But, because this model converges at a loss greater than the VGG16 model, it's likely that it is underfitting some, and could benefit from some extra capacity.
"""

    
qvars = bind_exercises(globals(), [
        Q1, Q2, Q3, Q4,
    ],
    var_format='q_{n}',
)

__all__ = list(qvars)
