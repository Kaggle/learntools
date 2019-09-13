from learntools.core import *

import geopandas as gpd

# Q1
world_loans = gpd.read_file("../input/geospatial-course-data/kiva_loans/kiva_loans.shp")

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
    def check(self):
        pass 

class Q3(EqualityCheckProblem):
    _vars = ["PHL", "PHL_loans"]
    _expected = [PHL, PHL_loans]
    _hint = ("Check out [this tutorial](https://www.kaggle.com/residentmario/indexing-selecting-assigning/), "
             "if you need to review conditional selection for DataFrames (and GeoDataFrames).")
    _solution = CS(
"""PHL = world.loc[world.iso_a3=="PHL"].copy()
PHL_loans = world_loans.loc[world_loans.country=="Philippines"].copy()
""")

class Q4P(CodingProblem):
    _hint = "Use the `plot()` method of each GeoDataFrame."
    _solution = CS(
"""ax = PHL.plot(figsize=(8,8), color='whitesmoke', linestyle=':', edgecolor='black')
PHL_loans.plot(ax=ax, markersize=2)
""")
    def check(self):
        pass
    
class Q4T(ThoughtExperiment):
    _hint = "Take a look at the map above.  Do all islands have loans?"
    _solution = ("The first thing that you can probably notice is that the map of the "
                 "Philippines is not very detailed, where many of the remote islands are "
                 "not included in the map.  But that said, it appears that **Mindoro** (in the "
                 "western part of the Philippines) is a large region without any loans "
                 "in the current dataset.  This island is potentially a good location for "
                 "recruiting new Field Partners!")
    
Q4 = MultipartProblem(Q4P, Q4T)

qvars = bind_exercises(globals(), [
    Q1, Q2, Q3, Q4
    ],
    tutorial_id=0,
    var_format='q_{n}',
    )
__all__ = list(qvars)
