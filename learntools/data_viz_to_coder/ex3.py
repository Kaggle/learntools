import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import warnings

from learntools.core import *

warnings.filterwarnings("ignore")
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
    _vars = ['high_score', 'worst_genre']
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
worst_genre = 'Simulation'
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
        
        container = passed_plt.axes().containers[0]
        
        assert type(container) == matplotlib.container.BarContainer, \
        "Is your figure a bar chart?  Please use `sns.barplot` to generate your figure."
        
        children = container.get_children()
        
        assert len(children) == 21, \
        "Your figure doesn't appear to have one bar for each platform."
               
        correct_bar_lengths = [7.0425, 6.6571428571428575, 5.897435897435898, 6.85263157894737,
                               6.9, 6.939622641509434, 6.038636363636365, 6.563636363636364, 
                               7.032417582417582, 6.773387096774192, 6.585064935064935, 
                               6.9785714285714295, 7.589999999999999, 6.401960784313727, 6.3, 
                               5.0116666666666685, 6.898305084745762, 7.021590909090909, 
                               6.996153846153844, 8.163636363636364, 7.315789473684211]
        
        assert [children[i].properties()['bbox'].width for i in range(21)] == correct_bar_lengths \
        or [children[i].properties()['bbox'].height for i in range(21)] == correct_bar_lengths, \
        "Did you select the `'Racing'` column?"

class ThinkRacing(ThoughtExperiment):
    _hint = ("Check the length of the bar corresponding to the **Wii** platform.  Does it appear to be "
             "longer than the other bars?  If so, you should expect a Wii game to perform well!")
    _solution = ("Based on the data, we should not expect a racing game for the Wii platform to receive "
                 "a high rating.  In fact, on average, racing games for Wii "
                 "score lower than any other platform.  Xbox One seems to be the best alternative, since "
                 "it has the highest average ratings.")
    
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
        
        children = passed_plt.axes().get_children()

        assert type(children[0]) == matplotlib.collections.QuadMesh, \
        "Is your figure a heatmap?  Please use `sns.heatmap` to generate your figure."
        
        assert len(children) == 263, \
        "Did you use all of the data in `ign_data` to create the heatmap?"

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
    var_format='step_{n}',
    )
__all__ = list(qvars)
