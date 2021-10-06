from learntools.core import *
import textwrap
import numpy as np

class MenuAnalysisPlan(ThoughtExperiment):
    _solution = """You could group reviews by what menu items they mention, and then calculate the average rating
    for reviews that mentioned each item. You can tell which foods are mentioned in reviews with low scores,
    so the restaurant can fix the recipe or remove those foods from the menu."""

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

    index_of_review_to_test_on = 14
    text_to_test_on = data.text.iloc[index_of_review_to_test_on]

    nlp = spacy.blank('en')
    review_doc = nlp(text_to_test_on)

    matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
    menu_tokens_list = [nlp(item) for item in menu]
    matcher.add("MENU", menu_tokens_list)
    matches = matcher(review_doc)"""))
    
    def check(self, matches):
        correct = [(2, 3), (16, 17), (58, 59)]
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
    from collections import defaultdict
    
    item_ratings = defaultdict(list)

    for idx, review in data.iterrows():
        doc = nlp(review.text)
        matches = matcher(doc)

        found_items = set([doc[match[1]:match[2]].text.lower() for match in matches])
        
        for item in found_items:
            item_ratings[item].append(review.stars)
    """))

    def check(self, item_ratings):
        correct = np.array([
            4.47058824, 4.15942029, 4.88888889, 4.33962264, 4.1796875 ,
            4.38888889, 4.40776699, 4.68      , 4.66666667, 4.44736842,
            4.48453608, 4.44444444, 4.5       , 4.23809524, 4.04761905,
            3.92      , 4.25      , 4.22      , 4.38095238, 3.8       ,
            4.        , 4.55555556, 3.4       , 4.45762712, 5.        ,
            5.        , 4.375     , 5.        , 4.54285714, 4.5       ,
            4.45454545, 4.12820513, 3.88888889, 4.30188679, 4.5       ,
            4.44444444, 4.75      , 4.48648649, 4.26315789, 4.        ,
            4.6       , 4.14285714, 5.
        ])

        means = np.array([sum(item)/len(item) for _, item in item_ratings.items()])
        means.sort()
        correct.sort()
        assert len(means) == len(correct), f"Please add items to item_ratings. You should have {len(correct)} items."
        assert np.allclose(means, correct)

class WorstReviewedItem(EqualityCheckProblem):
    _var = "worst_item"
    _hint = ("Loop through each item in item_ratings and calculate the mean, "
             "the sum of the ratings divided by the number of ratings. This is easiest "
             "using a dictionary comprehension. Then use the `sorted` function to sort "
             "the dictionary keys based on the dictionary values.")
    _solution = CS(textwrap.dedent("""
    # There are many ways to do this. Here is one.
    mean_ratings = {item: sum(ratings)/len(ratings) for item, ratings in item_ratings.items()}
    worst_item = sorted(mean_ratings, key=mean_ratings.get)[0]
    """))
    _expected = 'chicken cutlet'

class CountImportanceQuestion(ThoughtExperiment):
    _solution = """
    The less data you have for any specific item, the less you can trust that the average rating is the "real" sentiment of the customers. This is fairly common sense. If more people tell you the same thing, you're more likely to believe it. It's also mathematically sound. As the number of data points increases, the error on the mean decreases as 1 / sqrt(n).
    """

qvars = bind_exercises(globals(), [
    MenuAnalysisPlan,
    SingleReviewMatch,
    MatchAllDataset,
    WorstReviewedItem,
    CountImportanceQuestion
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
