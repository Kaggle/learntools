import math

import numpy as np

from learntools.core import *

class VectorAddition(CodingProblem):
    _var = 'legally_impossible'
    # TODO: Need to monkey patch is_attempted stuff (cf. one of the other emb ex modules)
    _default_values = [None]

    _solution = ("""
```python
legally_impossible = kv.most_similar(positive=['Legally Blonde', 'Mission: Impossible'])
```

Passing in two positive examples, `m1` and `m2`, finds the vectors that are most similar to `m1 + m2`. Semantically, this corresponds to movies that are about halfway between `m1` and `m2` in terms of meaning. 

In light of this interpretation, some of our `legally_impossible` results make a lot of sense. *Miss Congeniality*, *Mr. & Mrs. Smith*, and *Charlie's Angels* are all examples of movies that combine the "chick flick comedy" properties of *Legally Blonde* with the action/spy movie properties of *Mission: Impossible*.

What happens if we run something like `kv.most_similar(positive=['Legally Blonde', 'Legally Blonde'])`? We get the exact same results as `kv.most_similar('Legally Blonde')`. The reason comes down to our use of cosine distance. If we add a movie vector `m1` to itself, we get a vector that's twice as long, but its *angle* remains the same. So for any pair of movies `m1`, `m2`, `distance.cosine(m1, m2) == distance.cosine(m1+m1, m2)`.
""")

    def check(self, sim):
        assert_isinstance(list, sim, var='legally_impossible')
        assert len(sim), "Expected `legally_impossible` to be non-empty"
        v0 = sim[0]
        assert isinstance(v0, tuple), "Expected `legally_impossible` to be a list of tuples"
        titles, sims = zip(*sim)
        # TODO: Maybe more robust to inject kv and call most_similar on it ourselves to get expected value
        assert 'Miss Congeniality' in titles, "Expected `legally_impossible` to include movie *Miss Congeniality*"

class CalculateNorms(CodingProblem):
    _var = 'norms'
    _default_values = [None]

    _hint = ("Check out the axis keyword of np.linalg.norm in numpy's documentation: "
            "[https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.norm.html]"
            "(https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.norm.html)"
            )

    _solution = CS('norms = np.linalg.norm(w, axis=1)')

    def check(self, norms):
        n_movies = 26744
        assert_isinstance(np.ndarray, norms, var='norms')
        shape = norms.shape
        exp_shape = (n_movies,)
        assert shape == exp_shape, ("Expected `norms` to have shape `{}`"
                " (one norm value for each of {:,} movies). Actual shape"
                " was {}").format(exp_shape, n_movies, shape)
        norm0 = norms[0]
        exp = 2.0208979
        # Setting very generous rel_tol because of variability in training.
        assert math.isclose(norm0, exp, rel_tol=.5), ("Expected `norms[0]` to be"
                " approximately {}. Actual value: {}.").format(exp, norm0)

class NormColumn(CodingProblem):
    _var = 'all_movies_df'

    _solution = CS("all_movies_df['norm'] = norms")

    def check(self, df):
        assert_has_columns(df, ['norm'], var='all_movies_df')
        exp = 1.623779
        jum = df.loc[1, 'norm']
        assert math.isclose(exp, df.loc[1, 'norm'], rel_tol=.5), (
                "Expected norm column for movie 'Jumanji' to be {}"
                ". Was actually {}").format(exp, jum)


class NormPatterns(ThoughtExperiment):

    _solution = (
'''We have some movies whose embeddinging norms are 0 or very close to it - they also seem to be among the movies with the fewest ratings in the dataset.
This is consistent with what we'd expect from a model trained with an L2 weight penalty on embeddings - there's a cost to increasing an embedding's size.
Memorizing some properties of an obscure movie that only occurs once or twice in the dataset won't do much to decrease our overall error - so it's not worth 
paying the regularization cost.

On the other hand, the movies with the biggest embeddings are *not* necessarily the ones with the most ratings in the dataset. There's a strong trend of very
low average ratings in the list. Can you think of why this would be?
''')

VectorLengths = MultipartProblem(CalculateNorms, NormColumn, NormPatterns)

qvars = bind_exercises(globals(), [
    None,
    VectorAddition,
    VectorLengths
    ],
    var_format='part{n}',
)
__all__ = list(qvars)
