import pandas as pd
reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)


def check_q1(ans):
    expected = reviews.points.median()
    return ans == expected if type(ans) == float else False


def answer_q1():
    print("""reviews.points.median()""")


def check_q2(ans):
    expected = reviews.country.unique()
    return set(ans) == set(expected)


def answer_q2():
    print("""reviews.country.unique()""")


def check_q3(ans):
    expected = reviews.country.value_counts()
    return ans.equals(expected)


def answer_q3():
    print("""reviews.country.value_counts()""")


def check_q4(ans):
    median_price = reviews.price.median()
    expected = reviews.price.map(lambda v: v - median_price)
    return ans.equals(expected)


def answer_q4():
    print("""median_price = reviews.price.median()
reviews.price.map(lambda v: v - median_price)""")


def check_q5(ans):
    median_price = reviews.price.median()
    expected = reviews.price.apply(lambda x: x - median_price)
    return ans.equals(expected)


def answer_q5():
    print("""median_price = reviews.price.median()
reviews.price.apply(lambda v: v - median_price)""")


def check_q6(ans):
    expected = reviews.loc[(reviews.points / reviews.price).idxmax()].title
    return ans == expected


def answer_q6():
    print("""reviews.loc[(reviews.points / reviews.price).idxmax()].title""")


def check_q7(ans):
    tropical_wine = reviews.description.map(lambda r: "tropical" in r).value_counts()
    fruity_wine = reviews.description.map(lambda r: "fruity" in r).value_counts()
    expected = pd.Series([tropical_wine[True], fruity_wine[True]], index=['tropical', 'fruity'])
    return ans.plot.bar() if ans.equals(expected) else False


def answer_q7():
    print("""tropical_wine = reviews.description.map(lambda r: "tropical" in r).value_counts()
fruity_wine = reviews.description.map(lambda r: "fruity" in r).value_counts()
pd.Series([tropical_wine[True], fruity_wine[True]], index=['tropical', 'fruity'])
""")


def check_q8(ans):
    expected = reviews.loc[(reviews.country.notnull()) & (reviews.variety.notnull())]
    expected = expected.apply(lambda srs: srs.country + " - " + srs.variety, axis='columns')
    expected = expected.value_counts()
    return ans.head(10).plot.bar() if ans.head().equals(expected.head()) else False


def answer_q8():
    print("""ans = reviews.loc[(reviews.country.notnull()) & (reviews.variety.notnull())]
ans = ans.apply(lambda srs: srs.country + " - " + srs.variety, axis='columns')
ans.value_counts()""")
