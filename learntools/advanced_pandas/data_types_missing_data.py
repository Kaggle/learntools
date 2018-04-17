import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)


def check_q1(ans):
    expected = str(reviews.points.dtype)
    return str(ans) == expected if not isinstance(ans, pd.DataFrame) else False


def answer_q1():
    print("""reviews.points.dtype""")


def check_q2(ans):
    expected = reviews.price.astype(str)
    return ans.equals(expected)


def answer_q2():
    print("""reviews.price.astype(str)""")


def check_q3(ans):
    expected = reviews.price.isnull()
    return sns.countplot(ans) if ans.equals(expected) else False


def answer_q3():
    print("""reviews.price.isnull()""")


def check_q4(ans):
    expected = reviews.region_1.fillna("Unknown").value_counts()
    return ans.head().plot.bar() if ans.equals(expected) else False


def answer_q4():
    print("""reviews.region_1.fillna("Unknown").value_counts()""")


def check_q5(ans):
        return ans.plot.bar() if ans.equals(reviews.isnull().sum()) else False


def answer_q5():
    print("""reviews.isnull().sum()""")
