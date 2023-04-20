from learntools.core import *

import pandas as pd
import numpy as np
import fuzzywuzzy
from fuzzywuzzy import process
import charset_normalizer

#-----

# read in all our data
professors = pd.read_csv("../input/pakistan-intellectual-capital/pakistan_intellectual_capital.csv")

# set seed for reproducibility
np.random.seed(0)

# convert to lower case
professors['Country'] = professors['Country'].str.lower()
# remove trailing white spaces
professors['Country'] = professors['Country'].str.strip()

# get the top 10 closest matches to "south korea"
countries = professors['Country'].unique()
matches = fuzzywuzzy.process.extract("south korea", countries, limit=10, scorer=fuzzywuzzy.fuzz.token_sort_ratio)

def replace_matches_in_column(df, column, string_to_match, min_ratio = 47):
    # get a list of unique strings
    strings = df[column].unique()
    
    # get the top 10 closest matches to our input string
    matches = fuzzywuzzy.process.extract(string_to_match, strings, 
                                         limit=10, scorer=fuzzywuzzy.fuzz.token_sort_ratio)

    # only get matches with a ratio > 90
    close_matches = [matches[0] for matches in matches if matches[1] >= min_ratio]

    # get the rows of all the close matches in our dataframe
    rows_with_matches = df[column].isin(close_matches)

    # replace all rows with close matches with the input matches 
    df.loc[rows_with_matches, column] = string_to_match
    
    
replace_matches_in_column(df=professors, column='Country', string_to_match="south korea")
countries = professors['Country'].unique()

#----------

professors_q2 = professors.copy()
professors_q2['Graduated from'] = professors_q2['Graduated from'].str.strip()

professors_q3 = professors_q2.copy()
matches = fuzzywuzzy.process.extract("usa", countries, limit=10, scorer=fuzzywuzzy.fuzz.token_sort_ratio)
replace_matches_in_column(df=professors_q3, column='Country', string_to_match="usa", min_ratio=70)

####

class ExamineProvince(ThoughtExperiment):
    _hint = ("Use `unis = professors['Graduated from'].unique()` to take a look at "
             "the unique values in the 'Graduated from' column. You may find "
             "it useful to sort the data before printing it.")
    _solution = ('There are inconsistencies that can be fixed by removing white spaces '
                 'at the beginning and end of cells.  For instance, '
                 '"University of Central Florida" and " University of Central Florida" '
                 'both appear in the column.')
    
class TextProcessing(EqualityCheckProblem):
    _var = 'professors'
    _expected = professors_q2
    _hint = ("In the tutorial, you did the same operation on a different column.")
    _solution = CS(
"""professors['Graduated from'] = professors['Graduated from'].str.strip()
""")

class WorkingWithCities(EqualityCheckProblem):
    _var = 'professors'
    _expected = professors_q3
    _hint = ("Use the `replace_matches_in_column()` function defined above.")
    _solution = CS(
"""matches = fuzzywuzzy.process.extract("usa", countries, limit=10, scorer=fuzzywuzzy.fuzz.token_sort_ratio)
replace_matches_in_column(df=professors, column='Country', string_to_match="usa", min_ratio=70)
""")
               
qvars = bind_exercises(globals(), [
    ExamineProvince,
    TextProcessing,
    WorkingWithCities
    ],
    var_format='q{n}',
    )
__all__ = list(qvars)
