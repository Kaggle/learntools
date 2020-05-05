import pandas as pd

from learntools.core import *

reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)

# 1
class MedianPoints(EqualityCheckProblem):
    _var = 'median_points'
    _expected = reviews.points.median()
    _hint = "Use the `median` function (a built-in `pandas` function, like the `mean` function or the `unique` function)."
    _solution = CS('median_points = reviews.points.median()')

# 2
class UniqueCountries(CodingProblem):
    _var = 'countries'
    expected_set = set(reviews.country.unique())
    _hint = "Use the `unique` function to get a list of unique entries in a column."
    _solution = CS('countries = reviews.country.unique()')

    def check(self, countries):
        # TODO: implement this assert
        #assert_equal_ignoring_order(countries, self.expected_set, self._var)
        assert_len(countries, len(self.expected_set), var=self._var)
        assert set(countries) == self.expected_set, ("Incorrect value for "
                "`countries`: `{!r}`").format(countries)

# 3
class ReviewsPerCountry(EqualityCheckProblem):
    _var = 'reviews_per_country'
    _expected = reviews.country.value_counts()
    _hint = "To see a list of unique values and how often they occur in a Series, use the `value_counts` method."
    _solution = CS('reviews_per_country = reviews.country.value_counts()')

# 4
# TODO: This is an exact dupe of something shown in reference notebook
class CenteredPrice(EqualityCheckProblem):
    _var = 'centered_price'
    _expected = reviews.price - reviews.price.mean()
    _hint = "To get the mean of a column in a Pandas DataFrame, use the `mean` function."
    _solution = CS('centered_price = reviews.price - reviews.price.mean()')

# 5
class BargainWine(CodingProblem):
    _var = 'bargain_wine'
    _hint = "The `idxmax` method may be useful here."
    _solution = CS('''\
bargain_idx = (reviews.points / reviews.price).idxmax()
bargain_wine = reviews.loc[bargain_idx, 'title']''')

    def check(self, bargain_wine):
        assert_isinstance(str, bargain_wine, var='bargain_wine')
        # NB: Hard-coding these rather than calculating them dynamically.
        # These two wines are tied for best bargain, each having a points-to-price
        # ratio of 21.5. They'll always get the first one using the idxmax() solution,
        # but may get the Pinot if they use a different method.
        bargains = ['Bandit NV Merlot (California)', 'Cramele Recas 2011 UnWineD Pinot Grigio (Viile Timisului)']
        assert_is_one_of(bargain_wine, bargains, var='bargain_wine')

# 6
class DescriptorCounts(EqualityCheckProblem):
    _var = 'descriptor_counts'
    n_trop = reviews.description.map(lambda desc: "tropical" in desc).sum()
    n_fruity = reviews.description.map(lambda desc: "fruity" in desc).sum()
    _expected = pd.Series([n_trop, n_fruity], index=['tropical', 'fruity'])
    _hint = "Use a map to check each description for the string `tropical`, then count up the number of times this is `True`. Repeat this for `fruity`. Finally, create a `Series` combining the two values."
    _solution = CS('''\
n_trop = reviews.description.map(lambda desc: "tropical" in desc).sum()
n_fruity = reviews.description.map(lambda desc: "fruity" in desc).sum()
descriptor_counts = pd.Series([n_trop, n_fruity], index=['tropical', 'fruity'])''')

# 7
class StarRatings(EqualityCheckProblem):
    _var = 'star_ratings'
    _hint = "Begin by writing a custom function that accepts a row from the DataFrame as input and returns the star rating corresponding to the row.  Then, use `DataFrame.apply` to apply the custom function to every row in the dataset."
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
    )
__all__ = list(qvars)
