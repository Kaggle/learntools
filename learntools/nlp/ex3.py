import random

import numpy as np
import pandas as pd
import spacy
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split

from learntools.core import *

review_data = pd.read_csv('../input/nlp-course/yelp_ratings.csv')
nlp = spacy.load('en_core_web_lg')
all_vectors = np.load('../input/nlp-course/review_vectors.npy')

class TrainAModel(CodingProblem):
    _vars = ['model', 'X_test', 'y_test']
    _hint = ("Create the LinearSVC model with the regularization parameter = 10, "
    "the random state set to 1, and dual set to False. Then fit the model with the "
    "training features and labels."
    )
    _solution = CS("""
    model = LinearSVC(random_state=1, dual=False)
    model.fit(X_train, y_train)
    """)

    def check(self, model, X_test, y_test):
        model_score = model.score(X_test, y_test)
        assert model_score > 0.9, ("Your model accuracy should be about 94%. "
            "Instead it was {}. Something isn't right.".format(model_score))


class MakeAPrediction(EqualityCheckProblem):
    _var = "sentiment"
    _hint = ("You can get the review vector with the `nlp` model, then make a prediction "
    "with the trained model. Note that the model's `.predict()` method expects the input "
    "to have two dimensions. You'll need to reshape the review vector.")
    _solution = CS("""
    vector = nlp(review).vector.reshape((1, -1))
    sentiment = model.predict(vector)[0]
    """)
    _expected = 1

class CenteringVectors(ThoughtExperiment):
    _solution = """
    Sometimes your documents will already be fairly similar. For example, this data set
    is all reviews of businesses. There will be stong similarities between the documents
    compared to news articles, technical manuals, and recipes. You end up with all the
    similarities between 0.8 and 1 and no anti-similar documents (similarity < 0). When the
    vectors are centered, you are comparing documents within your dataset as opposed to all
    possible documents.
    """

class SimilarReview(EqualityCheckProblem):
    _var = "most_similar"
    _hint = ("To get the correct mean vector, you'll need to set the `axis` keyword "
    "argument to take the mean over the rows (dimension 0). The mean vector should be "
    "the same shape as the other document vectors, a 300-element vector. From there you "
    "can iterate through each centered vector and calculate the cosine simularity with "
    "the tea house review's vector. Finally to get the index of the most similar review, "
    "the `.argmax()` method is useful.")
    _solution = CS("""
    review_vec = nlp(review).vector

    ## Center the document vectors
    # Calculate the mean for the document vectors
    vec_mean = vectors.mean(axis=0)
    # Subtract the mean from the vectors
    centered = vectors - vec_mean

    # Calculate similarities for each document in the dataset
    # Make sure to subtract the mean from the review vector
    sims = np.array([cosine_similarity(review_vec - vec_mean, vec) for vec in centered])

    # Get the index for the most similar document
    most_similar = sims.argmax()
    """)
    _expected = 5930

class OtherSimilarReviews(ThoughtExperiment):
    _solution = """
    Reviews for coffee shops will also be similar to our tea house review because
    coffee and tea are semantically similar. Most cafes serve both coffee and tea
    so you'll see the terms appearing together often.
    """

qvars = bind_exercises(globals(), [
    TrainAModel,
    CenteringVectors,
    SimilarReview,
    OtherSimilarReviews
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
