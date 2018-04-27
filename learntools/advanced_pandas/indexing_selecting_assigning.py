import pandas as pd
import seaborn as sns

reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)


def check_q1(ans):
    expected = reviews.description
    return ans.equals(expected)


def answer_q1():
    print("""reviews.description""")


def check_q2(ans):
    expected = reviews.description[0]
    return ans == expected


def answer_q2():
    print("""reviews.description[0]""")


def check_q3(ans):
    expected = reviews.iloc[0]
    return ans.equals(expected)


def answer_q3():
    print("""reviews.iloc[0]""")


def check_q4(ans):
    expected = reviews.iloc[0:10, 1]
    return ans.equals(expected)


def answer_q4():
    print("""reviews.iloc[0:10, 1]""")


def check_q5(ans):
    expected = reviews.iloc[[1, 2, 3, 5, 8]]
    return ans.equals(expected)


def answer_q5():
    print("""reviews.iloc[[1, 2, 3, 5, 8]]""")


def check_q6(ans):
    expected = reviews.loc[[0, 1, 10, 100], ['country', 'province', 'region_1', 'region_2']]
    return ans.equals(expected)


def answer_q6():
    print("""reviews.loc[[0, 1, 10, 100], ['country', 'province', 'region_1', 'region_2']]""")


def check_q7(ans):
    expected = reviews.loc[0:99, ['country', 'variety']]
    return ans.equals(expected)


def answer_q7():
    print("""reviews.loc[0:99, ['country', 'variety']]""")


def check_q8(ans):
    expected = reviews.loc[reviews.country == 'Italy']
    return ans.equals(expected)


def answer_q8():
    print("""reviews.loc[reviews.country == 'Italy']""")


def check_q9(ans):
    expected = reviews.loc[reviews.region_2.notnull()]
    return ans.head().equals(expected.head())


def answer_q9():
    print("""reviews.loc[reviews.region_2.notnull()]""")


def check_q10(ans):
    expected = reviews.points
    return sns.countplot(ans) if ans.head().equals(expected.head()) else False


def answer_q10():
    print("""reviews.points""")


def check_q11(ans):
    expected = reviews.loc[:999, 'points']
    return sns.countplot(ans) if ans.head().equals(expected.head()) else False


def answer_q11():
    print("""reviews.loc[:999, 'points']""")


def check_q12(ans):
    expected = reviews.iloc[-1000:, 3]
    return sns.countplot(ans) if ans.head().equals(expected.head()) else False


def answer_q12():
    print("""reviews.iloc[-1000:, 3]""")


def check_q13(ans):
    expected = reviews[reviews.country == "Italy"].points
    return sns.countplot(ans) if ans.head().equals(expected.head()) else False


def answer_q13():
    print("""reviews[reviews.country == "Italy"].points""")


def check_q14(ans):
    expected = reviews[reviews.country.isin(["Italy", "France"]) & (reviews.points >= 90)].country
    return sns.countplot(ans) if ans.head().equals(expected.head()) else False


def answer_q14():
    print("""reviews[reviews.country.isin(["Italy", "France"]) & (reviews.points >= 90)].country""")
