import pandas as pd
import matplotlib
import seaborn as sns
#import matplotlib.pyplot as plt

from learntools.core import *

ign_data_soln = pd.read_csv('../input/ign.csv', index_col="id")

class LoadIGNData(EqualityCheckProblem):
    _var = 'ign_data'
    _expected = ign_data_soln
    _hint = "Use the `pd.read_csv()` function"
    _solution = CS('ign_data = pd.read_csv(ign_filepath, index_col="id")')
    
class ReviewData(EqualityCheckProblem):
    _vars = ['dragon_score', 'planet_date']
    _expected = [3, 12]
    _hint = "Use the `head()` command to print the first 5 rows. \
    **After printing the first 5 rows**, \
    each row corresponds to a different game, and game titles can be found in the `title` column. \
    The score for each game can be found in the `score` column. \
    The release date for each game can be found in the `release_day` column. \
    "
    _solution = CS(
"""# Print the first five rows of the data
ign_data.head()
# What was IGN's score for the September 2012 
# release of "Double Dragon: Neon" for Xbox 360?
dragon_score = 3.0
# Which day in September 2012 was "LittleBigPlanet PS Vita"
# for PlayStation Vita released? 
planet_date = 12
""")
    
class PlotMonths(CodingProblem):
    _var = 'plt'
    _hint = 'Use `sns.countplot()` and the `release_month` column of the `ign_data` DataFrame.'
    _solution = CS(
"""# Bar plot showing number of games released by month
sns.countplot(y=ign_data.release_month)
""")
    
    def solution_plot(self):
        self._view.solution()
        sns.countplot(y=ign_data_soln.release_month)
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, \
        "After you've written code to create a bar plot, `check()` will tell you whether your code is correct."
        
        print("Thank you for creating a plot!  To see how your code compares to the official solution, please use the code cell below.")
    
class LoadIGNScoreData(EqualityCheckProblem):
    _var = 'ign_scores'
    _expected = pd.read_csv('../input/ign_scores.csv', index_col="platform")
    _hint = "Use the `pd.read_csv()` function"
    _solution = CS('ign_scores = pd.read_csv(ign_scores_filepath, index_col="platform")')
    
qvars = bind_exercises(globals(), [
    LoadIGNData,
    ReviewData, 
    PlotMonths,
    LoadIGNScoreData
    ],
    tutorial_id=-1,
    var_format='step_{n}',
    )
__all__ = list(qvars)
