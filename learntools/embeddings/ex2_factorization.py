from learntools.core import *

import learntools.embeddings.solns.ex2_recommend_function as recc_solution_module
import learntools.embeddings.solns.ex2_recommend_nonobscure as recc_no_solution_module

class RecommendFunction(CodingProblem):
    _vars = ['recommend', 'model']

    _hint = (
'''I recommend breaking the function's implementation into the following steps:
1. Create a list/array containing all movie ids (from the `movies` dataframe)
2. Call model.predict() on a list/array with repeated copies of uid, and the sequence you created in step 1
3. Add the results of step 2 to the `movies` df as a new column, `"predicted_rating"`.
4. Sort on the column you added in step 3, and return the top `n` rows using the `head()` method.
''')

    _solution = CS.load(recc_solution_module.__file__)

    def check_whether_attempted(self, recommend, model):
        # A bit hacky. Attempted iff function body is non-empty.
        FunctionProblem.check_whether_attempted(recommend)

    def check(self, recommend, model):
        uid = 26556
        recc = recommend(model, uid, n=3)
        assert_has_columns(recc, ['movieId', 'predicted_rating'], 
                name="return value of `recommend`")
        assert_len(recc, 3, "result of calling `recommend` with `n=3`")
        # Could check sortedness, but not really an explicit requirement.
        # Erring on the side of false-correct judgements over false-incorrect.
        # Particulars of preloaded model may drift so dangerous to peg correctness
        # to specific model behaviour.
        # TODO: Could compare against behaviour of model.predict(), or test with
        # another dummy model having simple, predictable behaviour that we control.

class PredictionSanityCheck(ThoughtExperiment):
    _solution = (
'''I'm going to claim that these recommended movies are **bad**. In terms of genre and themes, our top picks don't seem like a great fit. But the most notable issue is that our top recommended movies are super-obscure, having only a handful of ratings each across the dataset. We just don't know much about these movies, so how can we be so confident that our target user will like them?

> **Aside:** You may have noticed another problem, which becomes very obvious when we look at the movies with 
the highest (or lowest) predicted scores: sometimes our model predicts values outside the allowable
range of 0.5-5 stars. For the purposes of recommendation, this is actually no problem: we only care about ranking
movies, not about the absolute values of their predicted scores. But this is still an interesting problem
to consider. How could we prevent our model from incurring needless errors by making predictions outside
the allowable range? Should we?''')

class FixingObscurity(ThoughtExperiment):
    _solution = (
'''One simple solution would be limiting our recommendations to movies with at least `n` ratings. This feels inelegant, in that we have to choose some arbitrary cut-off, and any reasonable choice will probably exclude some good recommendations. It would be nice if we could take into account popularity in a 'smoother' way. On the other hand, this is very simple to implement, and we don't even need to re-train our model, so it's worth a shot.

If we're willing to train a new model, there's another less hacky approach we can take which might fix our obscure recommendation problem *and* improve our overall accuracy at the same time: regularization. Specifically, putting an L2 weight penalty on our embeddings. I'll talk more about this in part 5 (and show how we would implement it).''')

class RecommendNonObscure(CodingProblem):
    _vars = ['recommend_nonobscure', 'model']
    _solution = CS.load(recc_no_solution_module.__file__)

    _hint = ("The `movies` dataframe has a column called `n_ratings`. You'll want to use "
            "a subset of movies filtered by the value of that column. (You can choose to "
            " do the filtering either before or after calculating predicted ratings.)")
    
    def check_whether_attempted(self, recommend, model):
        # A bit hacky. Attempted iff function body is non-empty.
        FunctionProblem.check_whether_attempted(recommend)
    
    def check(self, recommend, model):
        uid = 26556
        recc = recommend(model, uid, 3)
        assert_has_columns(recc, ['movieId', 'predicted_rating'], 
                name="return value of `recommend_nonobscure`")

class L2Intro(ThoughtExperiment):
    _solution = (
'''If a movie's embedding vector is all zeros, our model's output will always be zero (regardless of the user embedding vector). If you're not sure why, try reviewing the section of the tutorial on how the dot product of vectors is calculated.

Recall that an output value of 0 for our model corresponds to a predicted rating equal to the overall average in the training set (around 3.5 stars). This seems like a reasonable behaviour to tend toward for movies we have little information about.''')

class L2Predictions(CodingProblem):
    _var = 'l2_reccs'
    _default_values = [ [] ]

    _solution = CS('l2_reccs = recommend(l2_model, 26556)')

    def check_whether_attempted(self, *args):
        # This seems iffy.
        EqualityCheckProblem.check_whether_attempted(self, *args)

    def check(self, reccs):
        assert (reccs.iloc[:2].index == [228, 340]).all()

qvars = bind_exercises(globals(), [
    RecommendFunction,
    PredictionSanityCheck,
    FixingObscurity,
    RecommendNonObscure,
    L2Intro,
    L2Predictions,
    ],
    var_format='part{n}',
)
__all__ = list(qvars)
