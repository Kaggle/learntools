import pandas as pd

reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)
gaming_products = pd.read_csv("../input/things-on-reddit/top-things/top-things/reddits/g/gaming.csv")
gaming_products['subreddit'] = "r/gaming"
movie_products = pd.read_csv("../input/things-on-reddit/top-things/top-things/reddits/m/movies.csv")
movie_products['subreddit'] = "r/movies"
powerlifting_meets = pd.read_csv("../input/powerlifting-database/meets.csv")
powerlifting_competitors = pd.read_csv("../input/powerlifting-database/openpowerlifting.csv")


def check_q1(ans):
    expected = reviews.rename(columns={'region_1': 'region', 'region_2': 'locale'})
    return ans.head().equals(expected.head())


def answer_q1():
    print("""reviews.rename(columns={'region_1': 'region', 'region_2': 'locale'})""")


def check_q2(ans):
    expected = reviews.rename_axis("wines", axis="rows")
    return ans.head().equals(expected.head())


def answer_q2():
    print("""reviews.rename_axis("wines", axis="rows")""")


def check_q3(ans):
    expected = pd.concat([gaming_products, movie_products])
    return ans.equals(expected)


def answer_q3():
    print("""pd.concat([gaming_products, movie_products])""")


def check_q4(ans):
    expected = powerlifting_meets.set_index("MeetID").join(powerlifting_competitors.set_index("MeetID"))
    return ans.head().equals(expected.head())


def answer_q4():
    print("""powerlifting_meets.set_index("MeetID").join(powerlifting_competitors.set_index("MeetID"))""")
