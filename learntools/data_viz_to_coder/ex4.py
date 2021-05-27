import pandas as pd
import matplotlib
import seaborn as sns
import warnings

from learntools.core import *

warnings.filterwarnings("ignore")
df = pd.read_csv("../input/candy.csv", index_col="id")

class LoadData(EqualityCheckProblem):
    _var = 'candy_data'
    _expected = df
    _hint = ("Use `pd.read_csv`, and follow it with **two** pieces of text that "
             "are enclosed in parentheses and separated by commas.  (1) The "
             "filepath for the dataset is provided in `candy_filepath`.  (2) Use the "
             "`\"id\"` column to label the rows.")
    _solution = CS('candy_data = pd.read_csv(candy_filepath, index_col="id")')

class ReviewData(EqualityCheckProblem):
    _vars = ['more_popular', 'more_sugar']
    _expected = ['3 Musketeers', 'Air Heads']
    _hint = ("Use the `head()` command to print the first 5 rows. "
    "**After printing the first 5 rows**, "
    "each row corresponds to a different candy. "
    "The `'winpercent'` column indicates the popularity of the candy. "
    "The `'sugarpercent'` column has the amount of sugar in the candy.")
    _solution = CS(
"""# Print the first five rows of the data
candy_data.head()
# Which candy was more popular with survey respondents:
# '3 Musketeers' or 'Almond Joy'?
more_popular = '3 Musketeers'
# Which candy has higher sugar content: 'Air Heads'
# or 'Baby Ruth'?
more_sugar = 'Air Heads'
""")
    
class PlotBlueScatter(CodingProblem):
    _var = 'plt'
    _hint = ("Use `sns.scatterplot`, and set the variables for the x-axis and y-axis "
        "by using `x=` and `y=`, respectively.")
    _solution = CS(
"""# Scatter plot showing the relationship between 'sugarpercent' and 'winpercent'
sns.scatterplot(x=candy_data['sugarpercent'], y=candy_data['winpercent'])
""")

    def solution_plot(self):
        self._view.solution()
        sns.scatterplot(x=df['sugarpercent'], y=df['winpercent'])
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, "Please write code to create a scatter plot."
        
        children = passed_plt.gca().get_children()
        
        assert all(isinstance(x, matplotlib.spines.Spine) for x in children[1:5]), \
        "Is your figure a scatter plot? Please use `sns.scatterplot` to generate your figure."
        
class ThinkBlueScatter(ThoughtExperiment):
    _hint = ("Compare candies with higher sugar content (on the right side of the chart) to candies "
             "with lower sugar content (on the left side of the chart). Is one group clearly more "
             "popular than the other?")
    _solution = ("The scatter plot does not show a strong correlation between the two variables. "
                 "Since there is no clear relationship between the two variables, this tells us "
                 "that sugar content does not play a strong role in candy popularity.")
    
BlueScatter = MultipartProblem(PlotBlueScatter, ThinkBlueScatter)

class PlotBlueReg(CodingProblem):
    _var = 'plt'
    _hint = ("Use `sns.regplot`, and set the variables for the x-axis and y-axis "
             "by using `x=` and `y=`, respectively.")
    _solution = CS(
"""# Scatter plot w/ regression line showing the relationship between 'sugarpercent' and 'winpercent'
sns.regplot(x=candy_data['sugarpercent'], y=candy_data['winpercent'])
""")

    def solution_plot(self):
        self._view.solution()
        sns.regplot(x=df['sugarpercent'], y=df['winpercent'])
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, \
        "Please write code to create a scatter plot with a regression line."
        
        children = passed_plt.gca().get_children()
        
        assert all(isinstance(x, matplotlib.spines.Spine) for x in children[3:7]), \
        ("Is your figure a scatter plot with a regression line? "
         "Please use `sns.regplot` to generate your figure.")
        
class ThinkBlueReg(ThoughtExperiment):
    _hint = ("Does the regression line have a positive or negative slope?")
    _solution = ("Since the regression line has a slightly positive slope, this tells us that there "
                 "is a slightly positive correlation between `'winpercent'` and `'sugarpercent'`. "
                 "Thus, people have a slight preference for candies containing relatively more sugar.")

BlueReg = MultipartProblem(PlotBlueReg, ThinkBlueReg)

class ColorScatter(CodingProblem):
    _var = 'plt'
    _hint = ("Use `sns.scatterplot`, and set the variables for the x-axis, y-axis, and color "
        "of the points by using `x=`, `y=`, and `hue=`, respectively.")
    _solution = CS(
"""# Scatter plot showing the relationship between 'pricepercent', 'winpercent', and 'chocolate'
sns.scatterplot(x=candy_data['pricepercent'], y=candy_data['winpercent'], hue=candy_data['chocolate'])
""")

    def solution_plot(self):
        self._view.solution()
        sns.scatterplot(x=df['pricepercent'], y=df['winpercent'], hue=df['chocolate'])
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, \
        "After you've written code to create a scatter plot, `check()` will tell you whether your code is correct."

        legend_handles = passed_plt.figure(1).axes[0].get_legend_handles_labels()[0]
        
        assert all(isinstance(x, matplotlib.collections.PathCollection) for x in legend_handles), \
        ("Is your figure a scatter plot?  Please use `sns.scatterplot` to generate your figure.")
        
        #assert len(legend_handles) == 3, "Did you color-code the points with the `'chocolate'` column?"

class PlotColorReg(CodingProblem):
    _var = 'plt'
    _hint = ("Use `sns.lmplot`, and set the variables for the x-axis, y-axis, color of the points, "
             "and the dataset by using `x=`, `y=`, `hue=`, and `data=`, respectively.")
    _solution = CS(
"""# Color-coded scatter plot w/ regression lines
sns.lmplot(x="pricepercent", y="winpercent", hue="chocolate", data=candy_data)
""")

    def solution_plot(self):
        self._view.solution()
        sns.lmplot(x="pricepercent", y="winpercent", hue="chocolate", data=df)
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, \
        "After you've written code to create a scatter plot, `check()` will tell you whether your code is correct."
        
        legend_handles = passed_plt.figure(1).axes[0].get_legend_handles_labels()[0]
        
        assert all(isinstance(x, matplotlib.collections.PathCollection) for x in legend_handles), \
        ("Is your figure a scatter plot?  Please use `sns.scatterplot` to generate your figure.")
        
        assert len(legend_handles) == 2, \
        "Did you color-code the points with the `'chocolate'` column and add two regression lines?" 

class ThinkColorReg(ThoughtExperiment):
    _hint = "Look at each regression line - do you notice a positive or negative slope?"
    _solution = ("We'll begin with the regression line for chocolate candies. Since this line has "
                 "a slightly positive slope, we can say that more expensive chocolate candies tend to "
                 "be more popular (than relatively cheaper chocolate candies).  Likewise, "
                 "since the regression line for candies without chocolate has a negative slope, "
                 "we can say that if candies don't contain chocolate, they tend to be more popular "
                 "when they are cheaper.  One important note, however, is that the dataset "
                 "is quite small -- so we shouldn't invest too much trust in these patterns!  To "
                 "inspire more confidence in the results, we should add more candies to the dataset.")

ColorReg = MultipartProblem(PlotColorReg, ThinkColorReg)

class PlotSwarm(CodingProblem):
    _var = 'plt'
    _hint = ("Use `sns.swarmplot`, and set the variables for the x-axis and y-axis "
        "by using `x=` and `y=`, respectively.")
    _solution = CS(
"""# Scatter plot showing the relationship between 'chocolate' and 'winpercent'
sns.swarmplot(x=candy_data['chocolate'], y=candy_data['winpercent'])
""")

    def solution_plot(self):
        self._view.solution()
        sns.swarmplot(x=df['chocolate'], y=df['winpercent'])
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, "Please write code to create a categorical scatter plot."
        
        children = passed_plt.gca().get_children()
        
        assert all(isinstance(x, matplotlib.spines.Spine) for x in children[2:6]), \
        "Is your figure a categorical scatter plot?  Please use `sns.swarmplot` to generate your figure."
        
        #assert children[2].get_extents().ymax == -20.10169952441417, \
        #"Do you have `'chocolate'` on the x-axis and `'winpercent'` on the y-axis?" 
        
class ThinkSwarm(ThoughtExperiment):
    _hint = ("Which plot communicates more information?  In general, it's good practice to "
             "use the simplest plot that tells the entire story of interest.")
    _solution = ("In this case, the categorical scatter plot from **Step 7** is the more appropriate "
                 "plot. While both plots tell the desired story, the plot from **Step 6** conveys far "
                 "more information that could distract from the main point.")
    
Swarm = MultipartProblem(PlotSwarm, ThinkSwarm)

qvars = bind_exercises(globals(), [
    LoadData,
    ReviewData,
    BlueScatter,
    BlueReg,
    ColorScatter,
    ColorReg,
    Swarm
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
