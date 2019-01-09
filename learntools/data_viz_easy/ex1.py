import pandas as pd
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt

from learntools.core import *

filepath = '../input/museum_visitors.csv'
df = pd.read_csv(filepath, index_col="time", parse_dates=True)

class LoadMuseumData(EqualityCheckProblem):
    _var = 'museum_data'
    _expected = df
    _hint = "Use the `pd.read_csv()` function"
    _solution = CS('museum_data = pd.read_csv(museum_filepath, index_col="time", parse_dates=True)')
    
class ReviewData(EqualityCheckProblem):
    _vars = ['ca_museum_jul18', 'avila_oct18']
    _expected = [2620, 14658]
    _hint = "Use the `tail()` command to print the last five rows. \
    **After printing the last five rows**, \
    The number of visitors in July 2018 for each museum can be found in the row marked `2018-07-01`. \
    The number of visitors in October 2018 for each museum can be found in the row marked `2018-10-01`."
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
    _hint = 'Use `sns.lineplot()`, and plot one line for each column in the `museum_data` DataFrame.'
    _solution = CS(
"""# Line plot showing the number of visitors to each museum over time
sns.lineplot(data=museum_data)
""")
    
    def check(self, passed_plt):
        
        assert len(passed_plt.figure(1).axes) > 0, \
        "After you've written code to create a line plot, `check()` will tell you whether your code is correct."
        
        main_axis = passed_plt.figure(1).axes[0]
        legend_handles = main_axis.get_legend_handles_labels()[0]
        
        assert all(isinstance(x, matplotlib.lines.Line2D) for x in legend_handles), \
        "Is your figure a line plot?  Please use `sns.lineplot()` to generate the lines in your figure."

        assert len(legend_handles) == 4, \
        """Your plot does not seem to have 4 lines (one line for each museum). We detect %d lines.
        Note that we can only detect lines that appear in the legend, so please make sure that your
        legend has an entry for each line.
        """ % len(legend_handles)
        
class PlotAvila(CodingProblem):
    _var = 'plt'
    _solution = CS(
"""# PLOT 1: line plot showing the number of visitors to Avila Adobe over time
sns.lineplot(data=museum_data.avila_adobe, 
             label='avila_adobe')
""")
    _hint = 'Use `sns.lineplot()`.  Plot the `avila_adobe` column in the `museum_data` DataFrame.'

    def check(self, passed_plt):
        
        assert len(passed_plt.figure(1).axes) > 0, \
        "After you've written code to create a line plot, `check()` will tell you whether your code is correct."
        
        main_axis = passed_plt.figure(1).axes[0]
        legend_handles = main_axis.get_legend_handles_labels()[0]
        
        assert all(isinstance(x, matplotlib.lines.Line2D) for x in legend_handles), \
        "Is your figure a line plot?  Please use `sns.lineplot()` to generate the lines in your figure."
        
        assert len(legend_handles) == 1, \
        """Your plot does not seem to have a single line (for Avila Adobe only). We detect %d lines.
        Note that we can only detect lines that appear in the legend, so please make sure that your
        legend is nonempty.""" \
        % len(legend_handles)
        
        passed_y_vals = legend_handles[0].get_data()[1]
        soln_y_vals = df.loc[:, 'avila_adobe'].tolist()
        
        assert len(passed_y_vals) == len(soln_y_vals), \
        """Did you plot the number of visitors for each provided month in the dataset?  \
        We expected to see data for %d months, but it looks like you only plotted %d months.""" \
        % (len(soln_y_vals), len(passed_y_vals))
        
        assert all(passed_y_vals == soln_y_vals), \
        """Did you plot the correct column in the dataset?  You should plot the number of visitors to \
        Avila Adobe, but it looks like you might have selected a different museum."""

qvars = bind_exercises(globals(), [
    LoadMuseumData,
    ReviewData,
    PlotAll, 
    PlotAvila
    ],
    tutorial_id=118,
    var_format='step_{n}',
    )
__all__ = list(qvars)
