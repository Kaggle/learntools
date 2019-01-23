import pandas as pd
#import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt

from learntools.core import *

df = pd.read_csv('../input/ign.csv', index_col="Id")
df_scores = pd.read_csv('../input/ign_scores.csv', index_col="Platform")

class LoadIGNData(EqualityCheckProblem):
    _var = 'ign_data'
    _expected = df
    _hint = ("Use `pd.read_csv`, and follow it with **two** pieces of text that "
             "are enclosed in parentheses and separated by commas.  (1) The "
             "filepath for the dataset is provided in `ign_filepath`.  (2) Use the "
             "`\"Id\"` column to label the rows.")
    _solution = CS('ign_data = pd.read_csv(ign_filepath, index_col="Id")')
    
class ReviewData(EqualityCheckProblem):
    _vars = ['dragon_score', 'planet_date']
    _expected = [3, 12]
    _hint = ("Use `.head()` to print the first 5 rows. **After printing the "
             "first 5 rows**, each row corresponds to a different game, and game "
             "titles can be found in the `'Title'` column. The score for each game "
             "can be found in the `'Score'` column. The release date for each "
             "game can be found in the `'Release day'` column.")
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
    _hint = "Use `sns.countplot` and the `'Release month'` column of `ign_data`."
    _solution = CS(
"""# Bar chart showing number of games released by month
sns.countplot(y=ign_data['Release month'])
# Add title 
plt.title("Number of games released, by month")
# Add label for horizontal axis
plt.xlabel("")
# Add label for vertical axis
plt.ylabel("Month")
""")
    
    def solution_plot(self):
        self._view.solution()
        sns.countplot(y=df['Release month'])
        plt.xlabel("")
        plt.ylabel("Month")
        plt.title("Number of games released, by month")
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, \
        ("After you've written code to create a bar chart, `check()` will tell you whether your code "
         "is correct.")
        
        print("Thank you for creating a chart!  To see how your code compares to the official "
              "solution, please use the code cell below.")
        
class ThinkMonths(EqualityCheckProblem):
    _vars = ['month_most', 'month_least']
    _expected = [11, 7]
    _hint = ("Use the bar chart above.  For `month_most`, which month has the longest bar?  For "
             "`month_least`, which month has the shortest bar?")
    _solution = CS(
"""# According to the data, which month has the most 
# game releases? (Your answer should be a number between 1 and 12.)
month_most = 11
# According to the data, which month has the least 
# game releases? (Your answer should be a number between 1 and 12.)
month_least = 7
""")
    
Months = MultipartProblem(PlotMonths, ThinkMonths)
    
class LoadIGNScoreData(EqualityCheckProblem):
    _var = 'ign_scores'
    _expected = pd.read_csv('../input/ign_scores.csv', index_col="Platform")
    _hint = ("Use `pd.read_csv`, and follow it with **two** pieces of text that "
             "are enclosed in parentheses and separated by commas.  (1) The "
             "filepath for the dataset is provided in `ign_scores_filepath`.  (2) Use the "
             "`\"Platform\"` column to label the rows.")
    _solution = CS('ign_scores = pd.read_csv(ign_scores_filepath, index_col="Platform")')
    
class ThinkIGNScoreData(ThoughtExperiment):
    _hint = "h"
    _solution = "s"
    
IGNScoreData = MultipartProblem(LoadIGNScoreData, ThinkIGNScoreData)

class PlotRacing(CodingProblem):
    _var = 'plt'
    _hint = "Use `sns.barplot` and the `'Racing'` column of `ign_scores`."
    _solution = CS(
"""# Set the width and height of the figure
plt.figure(figsize=(8, 6))
# Bar chart showing average score for racing games by platform
sns.barplot(x=ign_scores['Racing'], y=ign_scores.index)
# Add label for horizontal axis
plt.xlabel("")
# Add label for vertical axis
plt.title("Average Score for Racing Games, by Platform")
""")
    
    def solution_plot(self):
        self._view.solution()
        plt.figure(figsize=(8, 6))
        sns.barplot(x=df_scores['Racing'], y=df_scores.index)
        plt.xlabel("")
        plt.title("Average Score for Racing Games, by Platform")
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, \
        ("After you've written code to create a bar chart, `check()` will tell you whether your code "
         "is correct.")
        
        print("Thank you for creating a chart!  To see how your code compares to the official "
              "solution, please use the code cell below.")    

class ThinkRacing(ThoughtExperiment):
    _hint = "h"
    _solution = "s"
    
Racing = MultipartProblem(PlotRacing, ThinkRacing)


class PlotHeat(CodingProblem):
    _var = 'plt'
    _hint = "Use `sns.heatmap`."
    _solution = CS(
"""# Set the width and height of the figure
plt.figure(figsize=(10,10))
# Heatmap showing average game score by platform and genre
sns.heatmap(ign_scores, annot=True)
# Add label for horizontal axis
plt.xlabel("Genre")
# Add label for vertical axis
plt.title("Average Game Score, by Platform and Genre")
""")
    
    def solution_plot(self):
        self._view.solution()
        plt.figure(figsize=(10,10))
        sns.heatmap(df_scores, annot=True)
        plt.xlabel("Genre")
        plt.title("Average Game Score, by Platform and Genre")
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, \
        ("After you've written code to create a heatmap, `check()` will tell you whether your code "
         "is correct.")
        
        print("Thank you for creating a chart!  To see how your code compares to the official "
              "solution, please use the code cell below.")    

class ThinkHeat(ThoughtExperiment):
    _hint = "h"
    _solution = "s"
    
Heat = MultipartProblem(PlotHeat, ThinkHeat)
    
qvars = bind_exercises(globals(), [
    LoadIGNData,
    ReviewData, 
    Months,
    IGNScoreData,
    Racing,
    Heat
    ],
    tutorial_id=-1,
    var_format='step_{n}',
    )
__all__ = list(qvars)
