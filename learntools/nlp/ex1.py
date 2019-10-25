from learntools.core import *
import textwrap
import numpy as np

class SingleReviewMatch(CodingProblem):
    _var = "matches"
    _hint = ("You should set the attr keyword argument to 'LOWER' so matching is case insensitive. "
             "An easy way to make a list of phrase documents is to loop through each item in the "
             "menu and apply the model nlp(item). This is best done in a list comprehension. "
             "From there, you can add the patterns to the matcher with matcher.add and pass in "
             "the review document to perform the matching.")
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
    _hint = ("For each review, use the `nlp` model to convert the text to a document. Then "
             "use the matcher from exercise 1 to extract the item matches from the review text. "
             "The matches you get from the matcher are tuples (match_id, start, end), so you can "
             "do doc[start:end] to get the text phrase for that match. To get all of the unique "
             "items in the review, create a list of all the matched phrases, and convert that "
             "into a set. Finally for each of those items, append the review's rating to " "item_ratings. Make sure to add the item string in lowercase. ")
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
        means.sort()
        correct.sort()
        assert len(means) == len(correct), f"Please add items to item_ratings. You should have {len(correct)} items."
        assert np.allclose(means, correct)

class BestReviewedItems(EqualityCheckProblem):
    _var = "best_items"
    _hint = ("Loop through each item in item_ratings and calculate the mean, "
             "the sum of the ratings divided by the number of ratings. This is easiest "
             "using a dictionary comprehension. Then use the `sorted` function to sort "
             "the dictionary keys based on the dictionary values.")
    _solution = CS(textwrap.dedent("""
    mean_ratings = {item: sum(ratings)/len(ratings) for item, ratings in item_ratings.items()}
    best_items = sorted(mean_ratings, key=mean_ratings.get, reverse=True)
    """))
    _expected = ['artichoke salad',
                'fettuccini alfredo',
                'turkey breast',
                'corned beef',
                'reuben',
                'pastrami',
                'chicken salad',
                'purista',
                'prosciutto',
                'chicken pesto',
                'chicken spinach salad',
                'grilled veggie',
                'gnocchi',
                'lasagna',
                'cheesesteak',
                'pizzas',
                'pasta',
                'mac and cheese',
                'calzone',
                'cannoli',
                'pizza',
                'tiramisu',
                'ziti',
                'chicken parmigiana',
                'salami',
                'italian sausage',
                'roast beef',
                'portobello',
                'meatball',
                'garlic bread',
                'italian beef',
                'tuna salad',
                'eggplant',
                'italian combo',
                'spaghetti',
                'turkey sandwich',
                'chicken cutlet']

class CountImportanceQuestion(ThoughtExperiment):
    _solution = """
    The less data you have for any specific item, the less you can trust that the average rating is the "real" sentiment of the customers. This is fairly common sense. If more people tell you the same thing, you're more likely to believe it. It's also mathematically sound. As the number of data points increases, the error on the mean decreases as 1 / sqrt(n).
    """

qvars = bind_exercises(globals(), [
    SingleReviewMatch,
    MatchAllDataset,
    BestReviewedItems,
    CountImportanceQuestion
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)