import pandas as pd
import seaborn as sns

reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)


def check_q1(ans):
    expected = reviews.groupby('taster_twitter_handle').taster_twitter_handle.count()
    return ans.equals(expected)


def answer_q1():
    print("""reviews.groupby('taster_twitter_handle').taster_twitter_handle.count()""")


def check_q2(ans):
    expected = reviews.groupby('price').points.max().sort_index()
    return ans.equals(expected)


def answer_q2():
    print("""reviews.groupby('price').points.max().sort_index()""")


def check_q3(ans):
    expected = reviews.groupby('variety').price.agg([min, max])
    return ans.equals(expected)


def answer_q3():
    print("""reviews.groupby('variety').price.agg([min, max])""")


def check_q4(ans):
    expected = reviews.groupby('taster_name').points.mean()
    return ans.plot.bar() if ans.equals(expected) else False


def answer_q4():
    print("""reviews.groupby('taster_name').points.mean()""")


def check_q5(ans):
    expected = reviews.groupby('variety').price.agg([min, max]).sort_values(by=['min', 'max'], ascending=False)
    return ans.head().plot.bar() if ans.head(10).equals(expected.head(10)) else False


def answer_q5():
    print("""reviews.groupby('variety').price.agg([min, max]).sort_values(by=['min', 'max'], ascending=False)""")


def check_q6(ans):
    expected = reviews.assign(n=0).groupby(['country', 'variety']).n.count().sort_values(ascending=False)
    return ans.head(10).plot.bar() if ans.head(10).equals(expected.head(10)) else False


def answer_q6():
    print("""reviews['n'] = 0
reviews.groupby(['country', 'variety']).n.count().sort_values(ascending=False)""")
