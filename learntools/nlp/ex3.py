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

class WordVectors(CodingProblem):
    _var = 'vectors'
    _hint = ("For each review use the `nlp` model to get the vectors. You can iterate "
    "through the reviews with the `.iterrows()` method. The easiest way to create the new "
    "numpy array is creating it from a list comprehension.")
    _solution = CS("""
    reviews = review_data[:100]

    with nlp.disable_pipes():
        vectors = np.array([nlp(review.text).vector for idx, review in reviews.iterrows()])""")
    
    def check(self, vectors):
        reviews = review_data[:100]
        with nlp.disable_pipes():
            vectors = np.array([nlp(review.text).vector for idx, review in reviews.iterrows()])

class TrainAModel(CodingProblem):
    _var = "model"
    _hint = ("Create the LinearSVC model with the regularization parameter = 10, "
    "the random state set to 1, and dual set to False. Then fit the model with the "
    "training features and labels."
    )
    _solution = CS("""
    model = LinearSVC(C=10, random_state=1, dual=False)
    model.fit(X_train, y_train)
    """)

    def check(self, model):
        X_train, X_test, y_train, y_test = train_test_split(all_vectors, review_data.sentiment, 
                                                            test_size=0.1, random_state=1)

        assert np.allclose(model.score(X_test, y_test), 0.9393667190657984)
                                    

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
    WordVectors,
    TrainAModel,
    MakeAPrediction,
    CenteringVectors,
    SimilarReview,
    OtherSimilarReviews
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)