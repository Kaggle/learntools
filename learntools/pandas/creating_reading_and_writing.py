import sqlite3

import pandas as pd

from learntools.core import *
from learntools.core.asserts import *
from learntools.core.richtext import CodeSolution as CS

class FruitDfCreation(EqualityCheckProblem):
    _var = 'fruits'
    _expected = (
            pd.DataFrame([[30, 21]], columns=['Apples', 'Bananas']),
    )
    _default_values = (None,)
    # TODO: This is a case where it would be nice to have a helper for creating 
    # a solution with multiple alternatives.
    _solution = CS(
            "fruits = pd.DataFrame([[30, 21]], columns=['Apples', 'Bananas'])"
    )

class FruitSalesDfCreation(EqualityCheckProblem):
    _var = 'fruit_sales'
    _default_values = (None,)
    _expected = (
            pd.DataFrame([[35, 21], [41, 34]], columns=['Apples', 'Bananas'],
                index=['2017 Sales', '2018 Sales']),
    )
    _solution = CS(
            """fruit_sales = pd.DataFrame([[35, 21], [41, 34]], columns=['Apples', 'Bananas'],
                index=['2017 Sales', '2018 Sales'])""",
            )

class RecipeSeriesCreation(EqualityCheckProblem):
    _var = 'ingredients'
    _default_values = (None,)
    quantities = ['4 cups', '1 cup', '2 large', '1 can']
    items = ['Flour', 'Milk', 'Eggs', 'Spam']
    recipe = pd.Series(quantities, index=items, name='Dinner')
    _expected = (
            recipe,
            )
    _solution = CS("""\
quantities = ['4 cups', '1 cup', '2 large', '1 can']
items = ['Flour', 'Milk', 'Eggs', 'Spam']
recipe = pd.Series(quantities, index=items, name='Dinner')""")

class ReadWineCsv(EqualityCheckProblem):
    _var = 'reviews'
    _default_values = (None,)
    _expected = (
            pd.read_csv('../input/wine-reviews/winemag-data_first150k.csv'),
    )
    _solution = CS("reviews = pd.read_csv('../input/wine-reviews/winemag-data_first150k.csv')")

class SaveAnimalsCsv(CodingProblem):

    _solution = CS('animals.to_csv("cows_and_goats.csv")')

    def check(self):
        path = 'cows_and_goats.csv'
        assert_file_exists(path)
        actual = pd.read_csv(path, index_col=0)
        expected = pd.DataFrame({'Cows': [12, 20], 'Goats': [22, 19]}, 
                index=['Year 1', 'Year 2'])
        assert_df_equals(actual, expected)

class ReadPitchforkSql(EqualityCheckProblem):
    _var = 'music_reviews'
    _default_values = (None,)
    # TODO: Is loading expected values expensive here? May want to do it on-demand 
    # when check is first called, rather than on import
    conn = sqlite3.connect("../input/pitchfork-data/database.sqlite")
    _expected = (
        pd.read_sql_query("SELECT * FROM artists", conn),
    )
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
    tutorial_id=-1,
    )
__all__ = list(qvars)
