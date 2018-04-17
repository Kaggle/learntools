import pandas as pd
chess_games = pd.read_csv("../input/chess/games.csv")
kepler = pd.read_csv("../input/kepler-exoplanet-search-results/cumulative.csv")
wine_reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)
ramen_reviews = pd.read_csv("../input/ramen-ratings/ramen-ratings.csv", index_col=0)


def check_q1(ans):
    expected = chess_games['winner'].value_counts() / len(chess_games)
    return ans.equals(expected)


def answer_q1():
    print("""chess_games['winner'].value_counts() / len(chess_games)""")


def check_q2(ans):
    expected = (chess_games
        .opening_name
        .map(lambda n: n.split(":")[0].split("|")[0].split("#")[0].strip())
        .value_counts()
    )
    return ans.equals(expected)


def answer_q2():
    print("""(chess_games
    .opening_name
    .map(lambda n: n.split(":")[0].split("|")[0].split("#")[0].strip())
    .value_counts()
)""")


def check_q3(ans):
    expected = (chess_games
         .assign(n=0)
         .groupby(['white_id', 'victory_status'])
         .n
         .apply(len)
         .reset_index()
)
    return ans.equals(expected)


def answer_q3():
    print("""(chess_games
    .assign(n=0)
    .groupby(['white_id', 'victory_status'])
    .n
    .apply(len)
    .reset_index()
)""")


def check_q4(ans):
    expected = (chess_games
        .assign(n=0)
        .groupby(['white_id', 'victory_status'])
        .n
        .apply(len)
        .reset_index()
        .pipe(lambda df: df.loc[df.white_id.isin(chess_games.white_id.value_counts().head(20).index)])
    )
    return ans.equals(expected)


def answer_q4():
    print("""(chess_games
    .assign(n=0)
    .groupby(['white_id', 'victory_status'])
    .n
    .apply(len)
    .reset_index()
    .pipe(lambda df: df.loc[df.white_id.isin(chess_games.white_id.value_counts().head(20).index)]) 
)""")


def check_q5(ans):
    expected = kepler.assign(n=0).groupby(['koi_pdisposition', 'koi_disposition']).n.count()

    return ans.plot.bar() if ans.equals(expected) else False


def answer_q5():
    print("""kepler.assign(n=0).groupby(['koi_pdisposition', 'koi_disposition']).n.count()""")


def check_q6(ans):
    expected = (((wine_reviews['points'].dropna() - 80) / 4)
     .value_counts()
     .sort_index()
     .rename_axis("Wine Ratings")
)
    return ans.plot.bar() if ans.head(10).equals(expected.head(10)) else False


def answer_q6():
    print("""(((wine_reviews['points'].dropna() - 80) / 4)
    .value_counts()
    .sort_index()
    .rename_axis("Wine Ratings")
)""")


def check_q7(ans):
    expected = (ramen_reviews
        .Stars
        .replace('Unrated', None)
        .dropna()
        .astype('float64')
        .value_counts()
        .rename_axis("Ramen Reviews")
        .sort_index())
    return ans.plot.bar() if ans.head(10).equals(expected.head(10)) else False


def answer_q7():
    print("""(ramen_reviews
    .Stars
    .replace('Unrated', None)
    .dropna()
    .astype('float64')
    .value_counts()
    .rename_axis("Ramen Reviews")
    .sort_index())""")


def check_q8(ans):
    expected = (ramen_reviews
     .Stars
     .replace('Unrated', None)
     .dropna()
     .astype('float64')
     .map(lambda v: round(v * 2) / 2)
     .value_counts()
     .rename_axis("Ramen Reviews")
     .sort_index()
)
    return ans.plot.bar() if ans.head(10).equals(expected.head(10)) else False


def answer_q8():
    print("""(ramen_reviews
     .Stars
     .replace('Unrated', None)
     .dropna()
     .astype('float64')
     .map(lambda v: round(v * 2) / 2)
     .value_counts()
     .rename_axis("Ramen Reviews")
     .sort_index()
)""")
