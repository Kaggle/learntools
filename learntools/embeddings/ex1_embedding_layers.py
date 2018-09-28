from tensorflow import keras

from learntools.core import *
from learntools.core.utils import bind_exercises
from learntools.core.problem import *
from learntools.core.richtext import *
from learntools.core.asserts import *

class WhyBiases(ThoughtExperiment):
    _solution = (
'''One basic observation is that adding biases gives our model more numbers to tune, and in this
sense it's strictly increasing its "capacity". This alone is a good enough reason to believe
adding biases will at least increase our accuracy on the training set (and possibly on the 
validation set, depending on how much we're already overfitting).

But we could also increase our model's capacity by just increasing the size of our embeddings, or
the number of hidden units. How does adding biases differ from that?''')

class WhatBiases(ThoughtExperiment):
    _solution = (
'''Some movies are, on average, rated significantly higher or lower than others. 
In the tutorial, I mentioned that predicting the average rating per-movie gave much
better results than always predicting the global average. Per-movie biases are a simple
way for our model to account for the relative goodness or badness of movies. 

If the model does utilize the biases in this way, then we should expect the highest biases
to go to highly acclaimed movies like *The Godfather* or *Schindler's List*, and the lowest
biases to go to stinkers like *Battlefield Earth* or *Sharknado*.

This relates to the question I posed above: how is adding biases to our model different from 
increasing its capacity by making the embedding vectors bigger or adding hidden units? Because 
our biases get added at the very end, our model has a lot less flexibility in how to use them. 
And this can be a good thing. At a high level, we're imposing a prior belief - that some movies
are intrinsically better or worse than others. This is a form of regularization!''')

BiasIntro = MultipartProblem(WhyBiases, WhatBiases)

class CodingBiases(CodingProblem):
    """TODO: How to test that they've properly added biases? Should confirm...
    - existence of an additional Embedding layer having movie_id_input as input, and output dimension of 1
    - that the output node (adding out and movie_bias) is unmolested
    - that the model has been compiled (the fact that they can do this without error basically shows they must have handled the extra dimension problem)
    """
    _vars = ['model_bias']

    _hint = (
'''
1. Surprisingly, this is another use case for an embedding layer. Check out the docs 
on [keras.layers.Embedding](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Embedding)
to review its parameters.
2. As with our existing use of Embedding layers, you may need to flatten its output to get rid of 
an extra dimension.''')

    show_solution_on_correct = False

    _solution = ('''*(Note: this is the code that should go in the "YOUR CODE GOES HERE" section, not the full model definition.)*

```python
bias_embedded = keras.layers.Embedding(df.movieId.max()+1, 1, input_length=1, name='bias',
                                      )(movie_id_input)
movie_bias = keras.layers.Flatten()(bias_embedded)
```
''')

    def check(self, model):
        # TODO: model topology introspection seems surprisingly tricky
        cfg = model.get_config()
        final = cfg['layers'][-1]
        assert final['class_name'] == 'Add', ('Expected final layer to have type Add,'
                ' but was {}'.format(final['class_name']))
        addends = final['inbound_nodes'][0]
        flat_bias_name = None
        for addend in addends:
            if addend[0] == 'prediction':
                continue
            flat_bias_name = addend[0]
        assert flat_bias_name is not None
        lookup = lambda name: [layer for layer in cfg['layers'] if layer['name'] == name][0]
        flat = lookup(flat_bias_name)
        bias_name = flat['inbound_nodes'][0][0][0]
        bias = lookup(bias_name)
        assert bias['class_name'] == 'Embedding'
        bc = bias['config']
        assert bc['input_length'] == 1
        assert bc['input_dim'] == 16715


class LoadingBiases(CodingProblem):
    _vars = ['bias_layer']
    _default_values = [None]

    _solution = ('''If you've given your bias layer a distinctive name, like 'bias', the following will work:

    bias_layer = model_bias.get_layer('bias')

Otherwise, you'll need to figure out what index your bias layer exists at (e.g. `bias_layer = model_bias.get_layer(index=8)`), or look up the name it was automatically assigned, e.g. `bias_layer = model_bias.get_layer('Embedding_1')`.''')
    
    show_solution_on_correct = False
    
    def check_whether_attempted(self, *args):
        # This seems iffy.
        EqualityCheckProblem.check_whether_attempted(self, *args)

    def check(self, bias_layer):
        assert_isinstance(keras.layers.Layer, bias_layer=bias_layer)
        assert_isinstance(keras.layers.Embedding, bias_layer=bias_layer)
        exp_shape = (None, 1, 1)
        assert bias_layer.output_shape == exp_shape, ("Expected bias layer to have"
                " output shape `{}`, but was actually `{}`".format(exp_shape,
                    bias_layer.output_shape))

class ExploringBiases(ThoughtExperiment):

    _solution = (
'''Directionally, these biases make sense. Highly rated movies have high biases, and poorly rated movies
have low biases. This agrees with the intuition discussed earlier about biases corresponding to goodness/badness.

But a problem sticks out. We're naively assigning biases which are approximately proportional to movies' 
average ratings - even for movies with few reviews. I'm not convinced that *Gray Lady Down* is the worst
movie ever based on *one* bad review. 

If you're shopping for a can opener, would you rather buy the one with a single 5-star review, or the one
with an average rating of 4.95 over 3,000 reviews? 

This is an especially important problem when dealing with sparse categorical data which can often have long tails
of rare values. We'll talk about an elegant solution to this problem - L2 regularization - in the next lesson.''')


qvars = bind_exercises(globals(), [
    BiasIntro,
    CodingBiases,
    None,
    LoadingBiases,
    ExploringBiases,
    None, # user biases
    ],
    tutorial_id=-1,
    var_format='part{n}',
)
__all__ = list(qvars)
