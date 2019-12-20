import pandas as pd
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt

from learntools.core import *

df = pd.read_csv("../input/fifa.csv", index_col="Date", parse_dates=True)

class FeedbackSys(EqualityCheckProblem):
    _var = 'one'
    _expected = 1
    _hint = ("How many moons does Earth have?")
    _solution = CS('one = 1')
    
class LoadFIFAData(EqualityCheckProblem):
    _var = 'fifa_data'
    _expected = df
    _hint = ("Use `pd.read_csv`, and follow it with **three** pieces of text that "
             "are enclosed in parentheses and separated by commas.  (1) The "
             "filepath for the dataset is provided in `fifa_filepath`.  (2) Use "
             "the `\"Date\"` column to label the rows. (3) Make sure that the row "
             "labels are recognized as dates.")
    _solution = CS('fifa_data = pd.read_csv(fifa_filepath, index_col="Date", parse_dates=True)')

class PlotLine(CodingProblem):
    _var = 'plt'
    _hint = ("Refer to the tutorial to see the solution.  The line of code that you need "
             " to fill in begins with `sns.lineplot`.")
    _solution = CS(
"""# Set the width and height of the figure
plt.figure(figsize=(16,6))

# Line chart showing how FIFA rankings evolved over time
sns.lineplot(data=fifa_data)
""")
    
    def solution_plot(self):
        self._view.solution()
        plt.figure(figsize=(16,6))
        sns.lineplot(data=df)
  
    def check(self, passed_plt):
        
        assert len(passed_plt.figure(1).axes) > 0, \
        ("After you've written code to create a line chart, `check()` will tell "
         "you whether your code is correct.")
        
        main_axis = passed_plt.figure(1).axes[0]
        legend_handles = main_axis.get_legend_handles_labels()[0]
        
        assert all(isinstance(x, matplotlib.lines.Line2D) for x in legend_handles), \
        ("Is your figure a line chart?  Please use `sns.lineplot()` to generate "
         "the lines in your figure.")

        assert len(legend_handles) == 6, \
        ("Your plot does not seem to have 6 lines (one line for each museum). "
         "We detect %d lines.") % len(legend_handles)
        
class ThinkLine(ThoughtExperiment):
    _hint = ("Which lines stay at least five consecutive years at the bottom of the chart?")
    _solution = ("The only country that meets this criterion is Brazil (code: BRA), as it "
                 "maintains the highest ranking in 1996-2000.  Other countries do spend some "
                 "time in the number 1 spot, but Brazil is the only country that maintains it "
                 "for at least five **consecutive** years.")
        
Line = MultipartProblem(PlotLine, ThinkLine)
       
qvars = bind_exercises(globals(), [
    FeedbackSys,
    LoadFIFAData,
    Line
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
