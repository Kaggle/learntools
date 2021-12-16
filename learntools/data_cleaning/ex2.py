from learntools.core import *

import pandas as pd
import numpy as np
from scipy import stats
from mlxtend.preprocessing import minmax_scaling
import seaborn as sns
import matplotlib.pyplot as plt

kickstarters_2017 = pd.read_csv("../input/kickstarter-projects/ks-projects-201801.csv")
np.random.seed(0)
original_goal_data = pd.DataFrame(kickstarters_2017.goal)
scaled_goal_data = minmax_scaling(original_goal_data, columns=['goal'])

class TryScaling(EqualityCheckProblem):
    _var = 'scaled_goal_data'
    _expected = scaled_goal_data
    _hint = "Use the `minimax_scaling()` function."
    _solution = CS(
"""scaled_goal_data = minmax_scaling(original_goal_data, columns=['goal'])
""")
    
class TryNormalization(ThoughtExperiment):
    _solution = ("The distributions in the normalized data look mostly the same.")
    _hint = """
Try running this code:

```python
# get the index of all positive pledges (Box-Cox only takes positive values)
index_positive_pledges = kickstarters_2017.pledged > 0

# get only positive pledges (using their indexes)
positive_pledges_only = kickstarters_2017.pledged.loc[index_positive_pledges]

# normalize the pledges (w/ Box-Cox)
normalized_values = pd.Series(stats.boxcox(positive_pledges_only)[0], 
                              name='pledged', index=positive_pledges_only.index)

# plot normalized data
ax = sns.histplot(normalized_values, kde=True)
ax.set_title("Normalized data")
```

"""
        
class NormOrScale(ThoughtExperiment):
    _hint = ("Do any of the examples use models that assume the data is normally distributed?")
    _solution = ("In the second example, scaling makes sense, so that "
                 "we can compare differences in jumping jacks and push-ups on equal footing.  As for the first example, "
                 "note that an older version of this course implied that normalization was required.  However, this is not the case.")
               
qvars = bind_exercises(globals(), [
    TryScaling,
    TryNormalization,
    NormOrScale,
    ],
    var_format='q{n}',
    )
__all__ = list(qvars)
