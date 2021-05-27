import pandas as pd
import matplotlib
import seaborn as sns
import warnings
import matplotlib.pyplot as plt

from learntools.core import *

warnings.filterwarnings("ignore")
df_b = pd.read_csv("../input/cancer_b.csv", index_col="Id")
df_m = pd.read_csv("../input/cancer_m.csv", index_col="Id")

class LoadCancerData(EqualityCheckProblem):
    _vars = ['cancer_b_data', 'cancer_m_data']
    _expected = [df_b, df_m]
    _hint = ("Use `pd.read_csv`, and follow it with **two** pieces of text that "
             "are enclosed in parentheses and separated by commas.  (1) The "
             "filepath for the dataset is provided in either `cancer_b_filepath` or "
             "`cancer_m_filepath`.  (2) Use the `\"Id\"` column to label the rows.")
    _solution = CS("""
cancer_b_data = pd.read_csv(cancer_b_filepath, index_col="Id")
cancer_m_data = pd.read_csv(cancer_m_filepath, index_col="Id")
""")

class ReviewData(EqualityCheckProblem):
    _vars = ['max_perim', 'mean_radius']
    _expected = [87.46, 20.57]
    _hint = ("Use the `head()` command to print the first 5 rows. "
             "**After printing the first 5 rows**, "
             "each row corresponds to a different tumor ID. "
             "The `'Perimeter (mean)'` column is the fourth column in the dataset. "
             "The `'Radius (mean)'` column is the second column.")
    _solution = CS(
"""# Print the first five rows of the (benign) data
cancer_b_data.head()
# Print the first five rows of the (malignant) data
cancer_m_data.head()
# In the first five rows of the data for benign tumors, what is the
# largest value for 'Perimeter (mean)'?
max_perim = 87.46
# What is the value for 'Radius (mean)' for the tumor with Id 842517?
mean_radius = 20.57
""")

class PlotHist(CodingProblem):
    _var = 'plt'
    _hint = ("Use `sns.distplot`, and set the data and legend label by using "
             "`a=` and `label=`, respectively. Set `kde=False`. You will need to " 
             "write two lines of code, corresponding to `cancer_m_data` and "
             "`cancer_b_data`.")
    _solution = CS(
"""# Histograms for benign and maligant tumors
sns.distplot(a=cancer_b_data['Area (mean)'], label="Benign", kde=False)
sns.distplot(a=cancer_m_data['Area (mean)'], label="Malignant", kde=False)
plt.legend()
""")

    def solution_plot(self):
        self._view.solution()
        sns.distplot(a=df_b['Area (mean)'], label="Benign", kde=False)
        sns.distplot(a=df_m['Area (mean)'], label="Malignant", kde=False)
        plt.legend()
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, "Please write code to create two histograms."
        
        children = passed_plt.gca().get_children()
        
        assert all(isinstance(x, matplotlib.patches.Rectangle) for x in children[:31]), \
        ("Does your figure contain two histograms?  Write two lines of code "
         "using `sns.distplot` to generate your figure.")

class ThinkHist(ThoughtExperiment):
    _hint = ("Does the histogram for malignant tumors appear mostly to the left or to the "
             "right of the histogram for benign tumors?  Which histogram appears wider?")
    _solution = ("Malignant tumors have higher values for `'Area (mean)'`, on average. "
                 "Malignant tumors have a larger range of potential values.")
    
Hist = MultipartProblem(PlotHist, ThinkHist)

class PlotThreshold(CodingProblem):
    _var = 'plt'
    _hint = ("Use `sns.kdeplot`, and specify the data and label by using `data=` and `label=`, "
             "respectively. You will need to write two lines of code, corresponding to "
             "`cancer_m_data` and `cancer_b_data`.")
    _solution = CS(
"""# KDE plots for benign and malignant tumors
sns.kdeplot(data=cancer_b_data['Radius (worst)'], shade=True, label="Benign")
sns.kdeplot(data=cancer_m_data['Radius (worst)'], shade=True, label="Malignant")
""")

    def solution_plot(self):
        self._view.solution()
        sns.kdeplot(data=df_b['Radius (worst)'], shade=True, label="Benign")
        sns.kdeplot(data=df_m['Radius (worst)'], shade=True, label="Malignant")
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, \
        "Please write code to create one figure containing two KDE plots."
        
        #children = passed_plt.gca().get_children()
        
        #assert all(isinstance(x, matplotlib.collections.PolyCollection) for x in children[0:2]) \
        #and all(isinstance(x, matplotlib.lines.Line2D) for x in children[2:4]), \
        #("Does your figure show two KDE plots?  Write two lines of code using "
        # "`sns.kdeplot` to generate your figure.")
        
class ThinkThreshold(ThoughtExperiment):
    _hint = ("Take a look at the KDE plots, and use the legend to tell the difference between "
             "malignant and benign tumors.  Around a value of 25, which curve appears higher?")
    _solution = ("The algorithm is more likely to classify the tumor as malignant. This is "
                 "because the curve for malignant tumors is much higher than the curve for benign "
                 "tumors around a value of 25 -- and an algorithm that gets high accuracy is likely "
                 "to make decisions based on this pattern in the data.")

Threshold = MultipartProblem(PlotThreshold, ThinkThreshold)
    
qvars = bind_exercises(globals(), [
    LoadCancerData,
    ReviewData,
    Hist,
    Threshold
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
