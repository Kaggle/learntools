from tensorflow import keras

from learntools.core import *

class ChooseEmbeddingVars(CodingProblem):
    _var = 'embedding_variables'
    _default_values = [{
            'stream_id',
            'user_id',
            'song_id',
            'timestamp',
            'artist_id',
            'song_duration',
            'explicit',
            'user_country',
        },]

    _solution = (
"""`user_id`, `song_id`, and `artist_id` all seem like useful features for this problem
which would be hard to handle without an embedding layer. They're sparse categorical features
with lots of possible values. Using an embedding layer for `user_country` isn't a bad idea
either, though we could probably also get away with one-hot encoding it (i.e. treating it
as 150 binary input variables).

What about the others?
- `stream_id` is basically just an index column - it won't be useful for prediction
- `timestamp` and `song_duration` are more or less continuous quantities, not categorical variables. We're better off treating them as numerical inputs (after some preprocessing)
- `explicit` only has two values. We might as well treat it as a binary input variable.
""")

    def check(self, evars):
        required = {'user_id', 'song_id', 'artist_id'}
        optional = {'user_country'}
        # TODO: Could be nice to give more fine-grained feedback here. e.g. just
        # tell them whether they have at least one fpos, and whether they have at least
        # one fneg.
        assert evars == required or evars == (required.union(optional))

class EmbeddingSizeInvestigation(ThoughtExperiment):

    _solution = (
"""Increasing the size of our embeddings increases our model's capacity. As usual, this comes with the benefit of potentially being able to recognize more complex patterns, increasing our accuracy... and the downside that our model might use this power to memorize overly-specific patterns that don't generalize well to unseen data. (Another downside: training will be a bit slower)

In this case, you likely saw that, with 32-d embeddings, our validation error goes down a little (if at all) and our training error goes down a lot - we're overfitting.

What's the optimal size for our movie and user embeddings? As with any hyperparameter, the only way to find out for sure is to experiment. [This TensorFlow tutorial](https://www.tensorflow.org/guide/feature_columns) gives a general rule of thumb for setting the embedding size of a categorical variable: the 4th root of the number of possible values. For our full dataset, this would mean 13-d movie embeddings and 19-d user embeddings. 
""")



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

class CodingBiases(ThoughtExperiment): # TODO: switch back to CodingProblem once checking properly implemented
    """TODO: How to test that they've properly added biases? Should confirm...
    - existence of an additional Embedding layer having movie_id_input as input, and output dimension of 1
    - that the output node (adding out and movie_bias) is unmolested
    - that the model has been compiled (the fact that they can do this without error basically shows they must have handled the extra dimension problem) <- jk, if they didn't flatten, they can still successfully compile. They only hit a problem when they try to train.

    Also, they can put the flatten() after the add instead of before, and that's
    also totally fine. Yeesh. Okay, maybe reqs are:
    - model output shape is (None, 1)
    - movie_bias exists, and is the output of a Layer instance, and if we follow it backward,
        we pass through an Embedding layer, and end up at movie_id_input
    And maybe if we find a lambda layer somewhere in movie_bias's ancestry, we 
    just throw up our arms and say "Ok, hopefully you know what you're doing"
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

This is a bit of a hack, in that we're using `keras.layers.Embedding` to implement
something that is not an "embedding" in any conventional sense. But it's en efficient
means to an end.
''')

    def TODO_check(self, model):
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
        assert bias['class_name'] == 'Embedding', ("Expected bias to have class Embedding, "
                "was {}").format(bias['class_name'])
        bc = bias['config']
        assert bc['input_length'] == 1, 'Expected bias to have input_length = 1'
        assert bc['input_dim'] == 16715, 'Expected bias to have input_dim = 16715'


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
        assert_isinstance(keras.layers.Layer, bias_layer, var='bias_layer')
        assert_isinstance(keras.layers.Embedding, bias_layer, var='bias_layer')
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

BigBiasProblem = MultipartProblem(
        WhyBiases, WhatBiases, 
        CodingBiases, 
        LoadingBiases, ExploringBiases,
        )

qvars = bind_exercises(globals(), [
    ChooseEmbeddingVars,
    EmbeddingSizeInvestigation,
    BigBiasProblem,
    ],
    var_format='part{n}',
)
__all__ = list(qvars)
