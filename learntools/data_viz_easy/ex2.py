import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from learntools.core import *

df = pd.read_csv('../input/ign_scores.csv', index_col="Platform")

class LoadIGNData(EqualityCheckProblem):
    _var = 'ign_data'
    _expected = df
    _hint = ("Use `pd.read_csv`, and follow it with **two** pieces of text that "
             "are enclosed in parentheses and separated by commas.  (1) The "
             "filepath for the dataset is provided in `ign_filepath`.  (2) Use the "
             "`\"Platform\"` column to label the rows.")
    _solution = CS('ign_data = pd.read_csv(ign_filepath, index_col="Platform")')
    
class ReviewData(EqualityCheckProblem):
    _vars = ['high_score', 'best_genre']
    _expected = [7.759930, 'Simulation']
    _hint = ("Use `ign_data` to print the entire dataset. **After printing the "
             "dataset**, each row corresponds to a different platform, and each "
             "genre has its own column. The entries contain the average score for each "
             "combination of genre and platform.")
    _solution = CS(
"""# Print the data
ign_data
# What is the highest average score received by PC games, for any platform?
high_score = 7.759930
# On the Playstation Vita platform, which genre has the 
# lowest average score? Please provide the name of the column, and put your answer 
# in single quotes (e.g., 'Action', 'Adventure', 'Fighting', etc.)
best_genre = 'Simulation'
""")
    
class PlotRacing(CodingProblem):
    _var = 'plt'
    _hint = "Use `sns.barplot` and the `'Racing'` column of `ign_data`."
    _solution = CS(
"""# Set the width and height of the figure
plt.figure(figsize=(8, 6))
# Bar chart showing average score for racing games by platform
sns.barplot(x=ign_data['Racing'], y=ign_data.index)
# Add label for horizontal axis
plt.xlabel("")
# Add label for vertical axis
plt.title("Average Score for Racing Games, by Platform")
""")
    
    def solution_plot(self):
        self._view.solution()
        plt.figure(figsize=(8, 6))
        sns.barplot(x=df['Racing'], y=df.index)
        plt.xlabel("")
        plt.title("Average Score for Racing Games, by Platform")
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, "Please write code to create a bar chart."
        
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
sns.heatmap(ign_data, annot=True)
# Add label for horizontal axis
plt.xlabel("Genre")
# Add label for vertical axis
plt.title("Average Game Score, by Platform and Genre")
""")
    
    def solution_plot(self):
        self._view.solution()
        plt.figure(figsize=(10,10))
        sns.heatmap(df, annot=True)
        plt.xlabel("Genre")
        plt.title("Average Game Score, by Platform and Genre")
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, "Please write code to create a heatmap."

        print("Thank you for creating a chart!  To see how your code compares to the official "
              "solution, please use the code cell below.")    

class ThinkHeat(ThoughtExperiment):
    _hint = ("To find the highest average ratings, look for the largest numbers (or lightest boxes) "
             "in the heatmap.  To find the lowest average ratings, find the smallest numbers (or "
             "darkest boxes).")
    _solution = ("**Simulation** games for **Playstation 4** receive the highest average ratings (9.2). "
                 "**Shooting** and **Fighting** games for **Game Boy Color** receive the lowest average "
                 "rankings (4.5).") 
    
Heat = MultipartProblem(PlotHeat, ThinkHeat)
    
qvars = bind_exercises(globals(), [
    LoadIGNData,
    ReviewData,
    Racing,
    Heat
    ],
    tutorial_id=-1,
    var_format='step_{n}',
    )
__all__ = list(qvars)
