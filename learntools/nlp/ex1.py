from learntools.core import *
import textwrap
import numpy as np

class SingleReviewMatch(CodingProblem):
    _var = "matches"
    _hint = ""
    _solution = CS(textwrap.dedent("""
    import spacy
    from spacy.matcher import PhraseMatcher

    nlp = spacy.load('en_core_web_sm')
    review_doc = nlp(data.iloc[4].text)

    matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
    patterns = [nlp(item) for item in menu]
    matcher.add("MENU", None, *patterns)
    matches = matcher(review_doc))"""))
    
    def check(self, matches):
        correct = [(6, 7), (51, 52), (70, 71), (98, 99)]
        assert [(match[1], match[2]) for match in matches] == correct

class MatchAllDataset(CodingProblem):
    _var = "item_ratings"
    _solution = CS(textwrap.dedent("""
    item_ratings = defaultdict(list)

    for idx, review in data.iterrows():
        doc = nlp(review.text)
        matches = matcher(doc)

        found_items = set([doc[match[1]:match[2]] for match in matches])
        
        for item in found_items:
            item_ratings[str(item).lower()].append(review.stars)
    """))

    def check(self, item_ratings):
        correct = np.array([4.444444444444445,
                            3.968421052631579,
                            4.888888888888889,
                            4.304469273743017,
                            4.079754601226994,
                            4.337078651685394,
                            4.392156862745098,
                            4.619047619047619,
                            4.641791044776119,
                            4.454545454545454,
                            4.335616438356165,
                            4.263636363636364,
                            3.909090909090909,
                            4.2592592592592595,
                            4.5,
                            4.0,
                            4.21875,
                            4.155172413793103,
                            4.0,
                            3.5454545454545454,
                            4.230769230769231,
                            3.8,
                            4.566666666666666,
                            5.0,
                            4.409638554216867,
                            5.0,
                            4.393939393939394,
                            5.0,
                            4.552631578947368,
                            4.444444444444445,
                            4.5,
                            4.021739130434782,
                            3.8536585365853657,
                            4.2105263157894735,
                            4.111111111111111,
                            4.6875,
                            4.8,
                            4.488888888888889,
                            4.238095238095238,
                            4.166666666666667,
                            4.666666666666667,
                            4.142857142857143,
                            5.0])

        means = np.array([sum(item)/len(item) for _, item in item_ratings.items()])
        assert np.allclose(means, correct)

qvars = bind_exercises(globals(), [
    SingleReviewMatch,
    MatchAllDataset
    ],
    tutorial_id=262,
    var_format='q_{n}',
    )
__all__ = list(qvars)