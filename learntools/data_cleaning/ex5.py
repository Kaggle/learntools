from learntools.core import *

import pandas as pd
import numpy as np
import fuzzywuzzy
from fuzzywuzzy import process
import chardet
suicide_attacks = pd.read_csv("../input/pakistansuicideattacks/PakistanSuicideAttacks Ver 11 (30-November-2017).csv", encoding='Windows-1252')
np.random.seed(0)

suicide_attacks['City'] = suicide_attacks['City'].str.lower()
suicide_attacks['City'] = suicide_attacks['City'].str.strip()

cities = suicide_attacks['City'].unique()
matches = fuzzywuzzy.process.extract("d.i khan", cities, limit=10, scorer=fuzzywuzzy.fuzz.token_sort_ratio)

def replace_matches_in_column(df, column, string_to_match, min_ratio = 90):
    strings = df[column].unique()
    matches = fuzzywuzzy.process.extract(string_to_match, strings, 
                                         limit=10, scorer=fuzzywuzzy.fuzz.token_sort_ratio)
    close_matches = [matches[0] for matches in matches if matches[1] >= min_ratio]
    rows_with_matches = df[column].isin(close_matches)
    df.loc[rows_with_matches, column] = string_to_match
    
replace_matches_in_column(df=suicide_attacks, column='City', string_to_match="d.i khan")

suicide_attacks_q2 = suicide_attacks.copy()
suicide_attacks_q2['Province'] = suicide_attacks_q2['Province'].str.lower()

suicide_attacks_q3 = suicide_attacks_q2.copy()
rows_with_matches = (suicide_attacks_q3['City'] == 'kuram agency')
suicide_attacks_q3.loc[rows_with_matches, 'City'] = 'kurram agency'

####

class ExamineProvince(ThoughtExperiment):
    _hint = ("Use `provinces = suicide_attacks['Province'].unique()` to take a look at "
             "the unique values in the 'Province' column.")
    _solution = ('According to Wikipedia, the **Balochistan** (also: **Baluchistan**) **region** '
                 'comprises the Pakistani province of **Balochistan**, the Iranian province of '
                 'Sistan and **Baluchestan**, and other areas.  It is not clear if "Balochistan" refers '
                 'to the region or the Pakistani province, and likewise, it is not clear if "Baluchistan" refers '
                 'to the region or the (Sistan and) Baluchestan Iranian province.  One way of checking for sure is to look at the '
                 'corresponding cities in the "cities" column, in each case. \n\nThat said, it seems '
                 'that both "FATA" and "Fata" refer to "Federally Administered Tribal Areas"; this is '
                 'an inconsistency in the data that can be easily fixed by making all entries in the column lowercase.')
    
class TextProcessing(EqualityCheckProblem):
    _var = 'suicide_attacks'
    _expected = suicide_attacks_q2
    _hint = ("In the tutorial, you converted every entry in a different column to lowercase.")
    _solution = CS(
"""suicide_attacks['Province'] = suicide_attacks['Province'].str.lower()
""")

class WorkingWithCities(EqualityCheckProblem):
    _var = 'suicide_attacks'
    _expected = suicide_attacks_q3
    _hint = ("Begin by isolating the rows with 'kuram agency' by creating a Pandas Series as follows: "
             "`rows_with_matches = (suicide_attacks['City'] == 'kuram agency')`.")
    _solution = CS(
"""rows_with_matches = (suicide_attacks['City'] == 'kuram agency')
suicide_attacks.loc[rows_with_matches, 'City'] = 'kurram agency'
""")
               
qvars = bind_exercises(globals(), [
    ExamineProvince,
    TextProcessing,
    WorkingWithCities
    ],
    var_format='q{n}',
    )
__all__ = list(qvars)
