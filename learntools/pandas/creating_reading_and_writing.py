import sqlite3

import pandas as pd

from learntools.core import *

class FruitDfCreation(EqualityCheckProblem):
    _var = 'fruits'
    _expected = (
            pd.DataFrame([[30, 21]], columns=['Apples', 'Bananas']),
    )
    # TODO: This is a case where it would be nice to have a helper for creating 
    # a solution with multiple alternatives.
    _hint = 'Use the `pd.DataFrame` constructor to create the DataFrame.'
    _solution = CS(
            "fruits = pd.DataFrame([[30, 21]], columns=['Apples', 'Bananas'])"
    )

class FruitSalesDfCreation(EqualityCheckProblem):
    _var = 'fruit_sales'
    _hint = 'Set the row labels in the DataFrame by using the `index` parameter in `pd.DataFrame`.'
    _expected = (
            pd.DataFrame([[35, 21], [41, 34]], columns=['Apples', 'Bananas'],
                index=['2017 Sales', '2018 Sales']),
    )
    _solution = CS(
            """fruit_sales = pd.DataFrame([[35, 21], [41, 34]], columns=['Apples', 'Bananas'],
                index=['2017 Sales', '2018 Sales'])""",
            )

class RecipeSeriesCreation(CodingProblem):
    _var = 'ingredients'
    quantities = ['4 cups', '1 cup', '2 large', '1 can']
    items = ['Flour', 'Milk', 'Eggs', 'Spam']
    recipe = pd.Series(quantities, index=items, name='Dinner')
    _hint = 'Note that the Series must be named `"Dinner"`. Use the `name` keyword-arg when creating your series.'
    _solution = CS("""\
quantities = ['4 cups', '1 cup', '2 large', '1 can']
items = ['Flour', 'Milk', 'Eggs', 'Spam']
recipe = pd.Series(quantities, index=items, name='Dinner')""")

    def check(self, ings):
        assert_series_equals(ings, self.recipe, var=self._var)
        assert ings.name == self.recipe.name, ("Expected `ingredients` to have"
                " `name={!r}`, but was actually `{!r}`").format(
                        self.recipe.name, ings.name)


class ReadWineCsv(EqualityCheckProblem):
    _var = 'reviews'
    _hint = ("Note that the csv file begins with an unnamed column of increasing integers. "
            "We want this to be used as the index. Check out the description of the `index_col` "
            "keyword argument in [the docs for `read_csv`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html).")
    _expected = pd.read_csv('../input/wine-reviews/winemag-data_first150k.csv', index_col=0)
    _solution = CS(
    "reviews = pd.read_csv('../input/wine-reviews/winemag-data_first150k.csv', index_col=0)"
    )

class SaveAnimalsCsv(CodingProblem):

    _solution = CS('animals.to_csv("cows_and_goats.csv")')
    _hint = 'Use [`to_csv`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_csv.html) to save a DataFrame to a CSV file.'

    def check(self):
        path = 'cows_and_goats.csv'
        assert_file_exists(path)
        actual = pd.read_csv(path, index_col=0)
        expected = pd.DataFrame({'Cows': [12, 20], 'Goats': [22, 19]}, 
                index=['Year 1', 'Year 2'])
        assert_df_equals(actual, expected, 
            name="Dataframe loaded from `cows_and_goats.csv`")

class ReadPitchforkSql(EqualityCheckProblem):
    _var = 'music_reviews'
    # TODO: Is loading expected values expensive here? May want to do it on-demand 
    # when check is first called, rather than on import
    conn = sqlite3.connect("../input/pitchfork-data/database.sqlite")
    _expected = (
        pd.read_sql_query("SELECT * FROM artists", conn),
    )
    _hint = 'After importing `sqlite3`, you first need to create a connector.  Then, you can supply an SQL statement to `pd.read_sql_query` to pull all of the data from the `artists` table.  For more information, check out the [Creating, Reading, and Writing Reference](https://www.kaggle.com/residentmario/creating-reading-and-writing-reference).'
    conn.close()

    _solution = CS("""\
import sqlite3
conn = sqlite3.connect("../input/pitchfork-data/database.sqlite")

music_reviews = pd.read_sql_query("SELECT * FROM artists", conn)""")


qvars = bind_exercises(globals(), [
    FruitDfCreation,
    FruitSalesDfCreation,
    RecipeSeriesCreation,
    ReadWineCsv,
    SaveAnimalsCsv,
    ReadPitchforkSql,
    ],
    )
__all__ = list(qvars)
