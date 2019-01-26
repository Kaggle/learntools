import pandas as pd
import matplotlib
import seaborn as sns

from learntools.core import *

df = pd.read_csv("../input/cancer.csv", index_col="Id")
df_b = pd.read_csv("../input/cancer_b.csv", index_col="Id")
df_m = pd.read_csv("../input/cancer_m.csv", index_col="Id")

class LoadCancerData(EqualityCheckProblem):
    _var = 'cancer_data'
    _expected = df
    _hint = ("Use `pd.read_csv`, and follow it with **two** pieces of text that "
             "are enclosed in parentheses and separated by commas.  (1) The "
             "filepath for the dataset is provided in `cancer_filepath`.  (2) Use the "
             "`\"Id\"` column to label the rows.")
    _solution = CS('cancer_data = pd.read_csv(cancer_filepath, index_col="Id")')

class ReviewData(EqualityCheckProblem):
    _vars = ['num_malig', 'mean_radius']
    _expected = [5, 20.57]
    _hint = ("Use the `head()` command to print the first 5 rows. "
    "**After printing the first 5 rows**, "
    "each row corresponds to a different tumor ID. "
    "The `'Diagnosis'` column is the first column in the dataset. "
    "The `'Radius (mean)'` column is the second column.")
    _solution = CS(
"""# Print the first five rows of the data
cancer_data.head()
# In the first five rows, how many tumors are malignant?
num_malig = 5
# What is the value for 'Radius (mean)' for the tumor with Id 842517?
mean_radius = 20.57
""")

class PlotScatter(CodingProblem):
    _var = 'plt'
    _hint = ("Use `sns.scatterplot`, and set the variables for the x-axis, y-axis, and color "
        "of the points by using `x=`, `y=`, and `hue=`, respectively.")
    _solution = CS(
"""# Scatter plot showing the relationship between 'Perimeter (mean)', 'Texture (worst)', and 'Diagnosis'
sns.scatterplot(x=cancer_data['Perimeter (mean)'], y=cancer_data['Texture (worst)'], hue=cancer_data['Diagnosis'])
""")

    def solution_plot(self):
        self._view.solution()
        sns.scatterplot(x=df['Perimeter (mean)'], y=df['Texture (worst)'], hue=df['Diagnosis'])
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, \
        "After you've written code to create a scatter plot, `check()` will tell you whether your code is correct."
        
        main_axis = passed_plt.figure(1).axes[0]
        legend_handles = main_axis.get_legend_handles_labels()[0]
        
        assert all(isinstance(x, matplotlib.collections.PathCollection) for x in legend_handles), \
        ("Is your figure a scatter plot?  Please use `sns.scatterplot` to generate your figure.")
        
        assert len(legend_handles) == 3, "Did you color-code the points with the `'Diagnosis'` column?"
                
class ThinkScatter(ThoughtExperiment):
    _hint = ("`'Perimeter (mean)'` is relatively useful if the malignant and benign "
             "tumors are separated relatively well in the scatter plot, where one type of tumor appears "
             "mostly on the **right** of the chart, and the other appears mostly on the **left**. "
             "Likewise, `'Texture (worst)'` is relatively useful if one type of tumor appears mostly "
             "towards the **top** of the chart, and the other appears mostly towards the **bottom**.")
    _solution = ("`'Perimeter (mean)'` is the relatively more useful column, since malignant tumors typically have "
                 "larger values in this column (and therefore appear mostly towards the right of the scatter plot). "
                 "While there's no perfect threshold that perfectly separates the two types of tumors, "
                 "the value of this column does provide _some_ indication of how the tumor should be diagnosed. "
                 "In contrast, `'Texture (worst)'` does not do as good of a job of separating the two types of tumors. "
                 "(_**Side Note**: In practice,  the most powerful algorithms are able to find patterns in the data "
                 "that are not immediately visible to humans -- so while it may not initially be obvious to "
                 "a human eye how `'Texture (worst)'` can be used to classify tumors, the machine learning algorithm may "
                 "be able to figure it out by studying all of the data to find more complex patterns "
                 "that involve multiple columns at once!_)")
    
Scatter = MultipartProblem(PlotScatter, ThinkScatter)

class SwarmPlot(CodingProblem):
    _var = 'plt'
    _hint = ("Use `sns.swarmplot`, and set the variables for the x-axis and y-axis "
        "by using `x=` and `y=`, respectively.")
    _solution = CS(
"""# Scatter plot showing the relationship between 'Diagnosis' and 'Perimeter (mean)'
sns.swarmplot(x=cancer_data['Perimeter (mean)'], y=cancer_data['Diagnosis'])
""")

    def solution_plot(self):
        self._view.solution()
        sns.swarmplot(x=df['Perimeter (mean)'], y=df['Diagnosis'])
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, "Please write code to create a categorical scatter plot."
        
        print("Thank you for creating a chart!  To see how your code compares to the official "
              "solution, please use the code cell below.")

class PlotThreshold(CodingProblem):
    _var = 'plt'
    _hint = ("Use `sns.kdeplot`, and specify the data and label by using `data=` and `label=`, respectively. You will need to "
             "write two lines of code, corresponding to `cancer_m_data` and `cancer_b_data`.")
    _solution = CS(
"""# KDE plot for benign and malignant tumors
sns.kdeplot(data=cancer_b_data['Radius (worst)'], shade=True, label="Benign")
sns.kdeplot(data=cancer_m_data['Radius (worst)'], shade=True, label="Malignant")
""")

    def solution_plot(self):
        self._view.solution()
        sns.kdeplot(data=df_b['Radius (worst)'], shade=True, label="Benign")
        sns.kdeplot(data=df_m['Radius (worst)'], shade=True, label="Malignant")
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, "Please write code to create a KDE plot."
        
        print("Thank you for creating a plot!  To see how your code compares to the official "
              "solution, please use the code cell below.")
        
class ThinkThreshold(ThoughtExperiment):
    _hint = ("Take a look at the KDE plot, and use the legend to tell the difference between malignant and benign tumors.  Does "
             "the curve for malignant tumors appear to the right (at higher values) or to the left (at lower values) of "
             "the curve for benign tumors?")
    _solution = ("Malignant tumors tend to have higher values for `'Radius (worst)'`.  This is something that we'd like a "
                 "machine learning algorithm to learn for itself when studying the data!")

Threshold = MultipartProblem(PlotThreshold, ThinkThreshold)
    
qvars = bind_exercises(globals(), [
    LoadCancerData,
    ReviewData,
    Scatter,
    SwarmPlot,
    Threshold
    ],
    tutorial_id=-1,
    var_format='step_{n}',
    )
__all__ = list(qvars)
