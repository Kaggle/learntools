import pandas as pd
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt

from learntools.core import *

file_path = '../input/museum_visitors.csv'
df = pd.read_csv(file_path, index_col="time", parse_dates=True)

class LoadMuseumData(EqualityCheckProblem):
    _var = 'museum_data'
    _expected = df
    _hint = "Use the `pd.read_csv()` function"
    _solution = CS('museum_data = pd.read_csv(museum_file_path)')
    
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
    _hint = 'Use `sns.lineplot()`, and set `data=museum_data`.'
    _solution = CS(
"""# Line plot showing the number of visitors to each museum over time
sns.lineplot(data=museum_data)
""")
    
    def check(self, passed_plt):
        main_axis = passed_plt.figure(1).axes[0]
        legend_labels = main_axis.get_legend_handles_labels()
        legend_soln = {'america_tropical_interpretive_center', 'firehouse_museum', 'avila_adobe', 'chinese_american_museum'}
        
        assert len(passed_plt.figure(1).axes) > 0, \
        "Remove the comment, and write code to create the line plot."
        #assert passed_plt.figure(1).axes[0].get_xlabel() == "time"

        assert all(isinstance(x, matplotlib.lines.Line2D) for x in legend_labels[0]), \
        """Is your figure a line plot?  Please use `sns.lineplot()` to generate the lines in your figure.
        """

        assert len(legend_labels[0]) == 4, \
        "Your plot does not seem to have 4 lines (one line for each museum). We detect %d lines." \
        % len(legend_labels[0])

        assert set(legend_labels[1]) == legend_soln, \
            """Please ensure that the labels match the titles of the columns. Your figure has the labels: 
            %s, 
            but we expect the labels to instead appear as follows: 
            %s.  
            """ \
            % (set(legend_labels[1]), legend_soln)
        
class PlotAvila(CodingProblem):
    _var = 'plt'
    _solution = CS(
"""# PLOT 1: line plot showing the number of visitors to Avila Adobe over time
sns.lineplot(data=museum_data.avila_adobe, 
             label='avila_adobe')
""")
    _hint = 'Use `sns.lineplot()`.  To plot only the column corresponding to Avila Adobe, set `data=museum_data.avila_adobe`.'

    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, \
        "Remove the comment, and write code to create the line plot."
        assert all(isinstance(x, matplotlib.lines.Line2D) for x in passed_plt.figure(1).axes[0].get_legend_handles_labels()[0]), \
        """Is your figure a line plot?  Please use `sns.lineplot()` to generate the lines in your figure.
        """
        assert len(passed_plt.figure(1).axes[0].get_legend_handles_labels()[0]) == 1, \
        "Your plot does not seem to have a single line (for Avila Adobe only). We detect %d lines." \
        % len(passed_plt.figure(1).axes[0].get_legend_handles_labels()[0])
        passed_y_vals = passed_plt.figure(1).axes[0].get_legend_handles_labels()[0][0].get_data()[1]
        soln_y_vals = df.loc[:, 'avila_adobe'].tolist()
        assert len(passed_y_vals) == len(soln_y_vals), "Did you plot the number of visitors for each provided month in the dataset?  We expected to see data for %d months, but it looks like you only plotted %d months." % (len(soln_y_vals), len(passed_y_vals))
        assert all(passed_y_vals == soln_y_vals), "Did you plot the correct column in the dataset?  You should plot the number of visitors to Avila Adobe, but it looks like you might have selected a different museum."

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
