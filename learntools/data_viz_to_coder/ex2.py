import pandas as pd
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt

from learntools.core import *

df = pd.read_csv('../input/museum_visitors.csv', index_col="Date", parse_dates=True)

class LoadMuseumData(EqualityCheckProblem):
    _var = 'museum_data'
    _expected = df
    _hint = ("Use `pd.read_csv`, and follow it with **three** pieces of text that "
             "are enclosed in parentheses and separated by commas.  (1) The "
             "filepath for the dataset is provided in `museum_filepath`.  (2) Use "
             "the `\"Date\"` column to label the rows. (3) Make sure that the row "
             "labels are recognized as dates.")
    _solution = CS('museum_data = pd.read_csv(museum_filepath, index_col="Date", parse_dates=True)')
    
class ReviewData(EqualityCheckProblem):
    _vars = ['ca_museum_jul18', 'avila_oct18']
    _expected = [2620, 14658]
    _hint = ("Use the `tail()` command that you learned about in the tutorial to print the "
             "last five rows. **After printing the last five rows**, the number of visitors "
             "in July 2018 for each museum can be found in the row marked `2018-07-01`, and the "
             "number of visitors in October 2018 for each museum can be found in "
             "the row marked `2018-10-01`.")
    _solution = CS(
"""# Print the last five rows of the data
museum_data.tail()
# How many visitors did the Chinese American Museum 
# receive in July 2018? 
ca_museum_jul18 = 2620
# In October 2018, how many more visitors did Avila 
# Adobe receive than the Firehouse Museum?
avila_oct18 = 14658
""")

class PlotAll(CodingProblem):
    _var = 'plt'
    _hint = ("Use `sns.lineplot`, and plot one line for each museum in "
             "`museum_data`. (_You can do this in a single line of code!_)")
    _solution = CS(
"""# Set the width and height of the figure
plt.figure(figsize=(12,6))
# Line chart showing the number of visitors to each museum over time
sns.lineplot(data=museum_data)
# Add title
plt.title("Monthly Visitors to Los Angeles City Museums")
""")
    
    def solution_plot(self):
        self._view.solution()
        plt.figure(figsize=(12,6))
        sns.lineplot(data=df)
        plt.title("Monthly Visitors to Los Angeles City Museums")
  
    def check(self, passed_plt):
        
        assert len(passed_plt.figure(1).axes) > 0, \
        ("After you've written code to create a line chart, `check()` will tell "
         "you whether your code is correct.")
        
        main_axis = passed_plt.figure(1).axes[0]
        legend_handles = main_axis.get_legend_handles_labels()[0]
        
        assert all(isinstance(x, matplotlib.lines.Line2D) for x in legend_handles), \
        ("Is your figure a line chart?  Please use `sns.lineplot()` to generate "
         "the lines in your figure.")

        assert len(legend_handles) == 4, \
        ("Your plot does not seem to have 4 lines (one line for each museum). "
         "We detect %d lines. Note that we can only detect lines that appear in "
         "the legend, so please make sure that your legend has an entry for each "
         "line by using `label=`.") % len(legend_handles)
        
class PlotAvila(CodingProblem):
    _var = 'plt'
    _solution = CS(
"""# Set the width and height of the figure
plt.figure(figsize=(12,6))
# Add title
plt.title("Monthly Visitors to Avila Adobe")
# Line chart showing the number of visitors to Avila Adobe over time
sns.lineplot(data=museum_data['Avila Adobe'])
# Add label for horizontal axis
plt.xlabel("Date")
""")
    _hint = ("Use `sns.lineplot` to plot the `\'Avila Adobe\'` column in "
             "`museum_data`. (_If you like, use `label=` to add the line "
             "to the legend, but this is not necessary!_)")
    
    def solution_plot(self):
        self._view.solution()
        plt.figure(figsize=(12,6))
        plt.title("Monthly Visitors to Avila Adobe")
        sns.lineplot(data=df['Avila Adobe'])
        plt.xlabel("Date")

    def check(self, passed_plt):
        
        assert len(passed_plt.figure(1).axes) > 0, \
        ("After you've written code to create a line chart, `check()` will tell "
         "you whether your code is correct.")
        
        main_axis = passed_plt.figure(1).axes[0]
        legend_handles = main_axis.get_legend_handles_labels()[0]
        
        assert all(isinstance(x, matplotlib.lines.Line2D) for x in legend_handles), \
        ("Is your figure a line chart?  Please use `sns.lineplot()` to generate "
         "the lines in your figure.")
        
        print("Thank you for creating a line chart!  To see how your code compares "
              "to the official solution, please use the code cell below.")
        
class ThinkAvila(ThoughtExperiment):
    _hint = ("Look at the early part of each year (around January).  Does the "
             "line chart dip to low values or reach relatively high values?")
    _solution = ("The line chart generally dips to relatively low values around "
                 "the early part of each year (in December and January), "
                 "and reaches its highest values in the middle of the year (especially "
                 "around May and June).  Thus, Avila Adobe usually gets more "
                 "visitors in March-August (or the spring and summer months).  With this in mind, "
                 "Avila Adobe could definitely benefit from hiring more seasonal "
                 "employees to help with the extra work in March-August (the spring and summer)!")
        
Avila = MultipartProblem(PlotAvila, ThinkAvila)
       
qvars = bind_exercises(globals(), [
    LoadMuseumData,
    ReviewData,
    PlotAll, 
    Avila
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
