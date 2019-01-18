import pandas as pd
import matplotlib
import seaborn as sns

from learntools.core import *

cancer_data_soln = pd.read_csv("../input/cancer.csv", index_col="Id")

class LoadCancerData(EqualityCheckProblem):
    _var = 'cancer_data'
    _expected = cancer_data_soln
    _hint = "Use the `pd.read_csv()` function"
    _solution = CS('cancer_data = pd.read_csv(cancer_filepath, index_col="Id")')

class ReviewData(EqualityCheckProblem):
    _vars = ['num_malig', 'mean_radius']
    _expected = [5, 20.57]
    _hint = ("Use the `head()` command to print the first 5 rows. "
    "**After printing the first 5 rows**, "
    "each row corresponds to a different tumor ID. "
    "The `'Diagnosis'` column is the first column in the dataset. "
    "The `'Radius (mean)'` column is the second column in the dataset. "
    )
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
    _hint = ("Use `sns.scatterplot()`, and set the variables for the x-axis, y-axis, and color "
        "of the points by using `x=`, `y=`, and `hue=`, respectively.")
    _solution = CS(
"""# Scatter plot showing the relationship between 'Radius (worst)', 'Texture (worst)', and 'Diagnosis'
sns.scatterplot(x=cancer_data['Radius (worst)'], y=cancer_data['Texture (worst)'], hue=cancer_data['Diagnosis'])
""")

    def solution_plot(self):
        self._view.solution()
        sns.scatterplot(x=cancer_data_soln['Radius (worst)'], y=cancer_data_soln['Texture (worst)'], 
            hue=cancer_data_soln['Diagnosis'])
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, \
        "After you've written code to create a bar plot, `check()` will tell you whether your code is correct."
        
        print("Thank you for creating a plot!  To see how your code compares to the official solution, please use the code cell below.")
   

qvars = bind_exercises(globals(), [
    LoadCancerData,
    ReviewData,
    PlotScatter
    ],
    tutorial_id=-1,
    var_format='step_{n}',
    )
__all__ = list(qvars)
