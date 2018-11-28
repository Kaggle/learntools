import pandas as pd

from learntools.core import *

reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)

class MedianPoints(EqualityCheckProblem):
    _var = 'median_points'
    _expected = reviews.points.median()
    _solution = CS('median_points = reviews.points.median()')

class UniqueCountries(CodingProblem):
    _var = 'countries'
    expected_set = set(reviews.country.unique())
    _solution = CS('countries = reviews.country.unique()')

    def check(self, countries):
        # TODO: implement this assert
        #assert_equal_ignoring_order(countries, self.expected_set, self._var)
        assert_len(countries, len(self.expected_set), self._var)
        assert set(countries) == self.expected_set, ("Incorrect value for"
                "`countries`: `{!r}`").format(countries)

class ReviewsPerCountry(EqualityCheckProblem):
    _var = 'reviews_per_country'
    _expected = reviews.country.value_counts()
    _solution = CS('reviews_per_country = reviews.country.value_counts()')

# TODO: This is an exact dupe of something shown in reference notebook
class CenteredPrice(EqualityCheckProblem):
    _var = 'centered_price'
    _expected = reviews.price - reviews.price.mean()
    _solution = CS('centered_price = reviews.price - reviews.price.mean()')

class BargainWine(EqualityCheckProblem):
    _var = 'bargain_wine'
    _expected = reviews.loc[(reviews.points / reviews.price).idxmax(), 'title']
    _solution = CS('''\
bargain_idx = (reviews.points / reviews.price).idxmax()
bargain_wine = reviews.loc[bargain_idx, 'title']''')

class DescriptorCounts(EqualityCheckProblem):
    _var = 'descriptor_counts'
    n_trop = reviews.description.map(lambda desc: "tropical" in desc).sum()
    n_fruity = reviews.description.map(lambda desc: "fruity" in desc).sum()
    _expected = pd.Series([n_trop, n_fruity], index=['tropical', 'fruity'])
    _solution = CS('''\
n_trop = reviews.description.map(lambda desc: "tropical" in desc).sum()
n_fruity = reviews.description.map(lambda desc: "fruity" in desc).sum()
descriptor_counts = pd.Series([n_trop, n_fruity], index=['tropical', 'fruity'])''')

class StarRatings(EqualityCheckProblem):
    # TODO: hint
    _var = 'star_ratings'

    _solution = CS("""\
def stars(row):
    if row.country == 'Canada':
        return 3
    elif row.points >= 95:
        return 3
    elif row.points >= 85:
        return 2
    else:
        return 1
    
star_ratings = reviews.apply(stars, axis='columns')""")

    def stars_transform(row):
        if row.country == 'Canada':
            return 3
        elif row.points >= 95:
            return 3
        elif row.points >= 85:
            return 2
        else:
            return 1
    
    # NB: This is kind of slow. Might want to lazy-initialize.
    _expected = reviews.apply(stars_transform, axis='columns')


qvars = bind_exercises(globals(), [
    MedianPoints,
    UniqueCountries,
    ReviewsPerCountry,
    CenteredPrice,
    BargainWine,
    DescriptorCounts,
    StarRatings,
    ],
    tutorial_id=47,
    )
__all__ = list(qvars)
