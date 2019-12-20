from learntools.core import *

import geopandas as gpd

congrats_map_completion = "Thank you for creating a map!"
correct_message_map_completion = ""

# Q1
world_loans = gpd.read_file("../input/geospatial-learn-course-data/kiva_loans/kiva_loans/kiva_loans.shp")

# Q3
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
PHL = world.loc[world.iso_a3=="PHL"].copy()
PHL_loans = world_loans.loc[world_loans.country=="Philippines"].copy()

class Q1(EqualityCheckProblem):
    _var = "world_loans"
    _expected = world_loans
    _hint = "Use `gpd.read_file()`."
    _solution = CS(
"""# Load the data
world_loans = gpd.read_file(loans_filepath)
""")

class Q2(CodingProblem):
    _hint = "Use the `plot()` method of each GeoDataFrame."
    _solution = CS(
"""ax = world.plot(figsize=(20,20), color='whitesmoke', linestyle=':', edgecolor='black')
world_loans.plot(ax=ax, markersize=2)
""")
    _congrats = congrats_map_completion
    _correct_message = correct_message_map_completion
    def check(self):
        pass 

class Q3(EqualityCheckProblem):
    _var = "PHL_loans"
    _expected = PHL_loans
    _hint = ("Check out [this tutorial](https://www.kaggle.com/residentmario/indexing-selecting-assigning/), "
             "if you need to review conditional selection for DataFrames (and GeoDataFrames).")
    _solution = CS(
"""PHL_loans = world_loans.loc[world_loans.country=="Philippines"].copy()
""")

class Q4P(CodingProblem):
    _hint = "Use the `plot()` method of each GeoDataFrame."
    _solution = CS(
"""ax = PHL.plot(figsize=(12,12), color='whitesmoke', linestyle=':', edgecolor='lightgray')
PHL_loans.plot(ax=ax, markersize=2)
""")
    _congrats = congrats_map_completion
    _correct_message = correct_message_map_completion
    def check(self):
        pass
    
class Q4T(ThoughtExperiment):
    _hint = "Take a look at the map above.  Do all islands have loans?"
    _solution = ("There are a number of potential islands, but **Mindoro** (in the "
                 "central part of the Philippines) stands out as a relatively large island without any loans "
                 "in the current dataset.  This island is potentially a good location for "
                 "recruiting new Field Partners!")
    
Q4 = MultipartProblem(Q4P, Q4T)

qvars = bind_exercises(globals(), [
    Q1, Q2, Q3, Q4
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
