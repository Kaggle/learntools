from learntools.core import *

import geopandas as gpd

congrats_map_completion = "Thank you for creating a map!"
correct_message_map_completion = ""

collisions = gpd.read_file("../input/geospatial-learn-course-data/NYPD_Motor_Vehicle_Collisions/NYPD_Motor_Vehicle_Collisions/NYPD_Motor_Vehicle_Collisions.shp")
hospitals = gpd.read_file("../input/geospatial-learn-course-data/nyu_2451_34494/nyu_2451_34494/nyu_2451_34494.shp")

class Q1(CodingProblem):
    _hint = ("Use `folium.plugins.HeatMap()` to add a heatmap. Set `data` to a DataFrame containing the latitude "
        "and longitude locations.  We got fairly good results by setting `radius=9`. Don't forget "
        "to add it to the map with the `add_to()` method!")
    _solution = CS(
"""# Visualize the collision data
HeatMap(data=collisions[['LATITUDE', 'LONGITUDE']], radius=9).add_to(m_1)
""")
    _congrats = congrats_map_completion
    _correct_message = correct_message_map_completion
    def check(self):
        pass

class Q2(CodingProblem):
    _hint = "Use `folium.Marker()` to add a marker for each hospital location."
    _solution = CS(
"""# Visualize the hospital locations
for idx, row in hospitals.iterrows():
    Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m_2)
""")
    _congrats = congrats_map_completion
    _correct_message = correct_message_map_completion
    def check(self):
        pass 

class Q3(CodingProblem):
    _var = "outside_range"
    _hint = ("Begin by creating a buffer of size 10000 around each point in `hospitals.geometry`. "
             "Then, use the `unary_union` attribute to create a MultiPolygon object, before checking "
             "to see if it contains each collision.")
    _solution = CS(
"""coverage = gpd.GeoDataFrame(geometry=hospitals.geometry).buffer(10000)
my_union = coverage.geometry.unary_union
outside_range = collisions.loc[~collisions["geometry"].apply(lambda x: my_union.contains(x))]
""")
    def check(self, results):
        coverage = gpd.GeoDataFrame(geometry=hospitals.geometry).buffer(10000)
        my_union = coverage.geometry.unary_union
        outside_range = collisions.loc[~collisions["geometry"].apply(lambda x: my_union.contains(x))]   
        assert set(outside_range.columns)==set(results.columns), \
        ("The column names in `outside_range` should match the column names in `collisions` (to create "
         "don't add or `outside range`, you shoul not add or remove any columns.")
        assert len(outside_range)==len(results), "`outside_range` does not have the correct number of rows."

class Q4(FunctionProblem):
    _var = "best_hospital"
    _test_cases =  [
            ( collisions.geometry.iloc[0], "CALVARY HOSPITAL INC"),
            ( collisions.geometry.iloc[1], "QUEENS HOSPITAL CENTER"),
            ( collisions.geometry.iloc[2], "MONTEFIORE MEDICAL CENTER-WAKEFIELD HOSPITAL")
            ]
    _hint = ("Use the `distance()` method of `hospitals.geometry`.")
    _solution = CS(
"""def best_hospital(collision_location):
    idx_min = hospitals.geometry.distance(collision_location).idxmin()
    my_hospital = hospitals.iloc[idx_min]
    name = my_hospital["name"]
    return name
""")    

class Q5(CodingProblem):
    _var = "highest_demand"
    _hint = ("Begin by applying the `best_hospital()` function to every entry in `outside_range.geometry`.")
    _solution = CS(
"""highest_demand = outside_range.geometry.apply(best_hospital).value_counts().idxmax()

""")
    def check(self, submitted):
        assert type(submitted)==str, "Your answer must be a Python string."
        assert (submitted in list(hospitals.name.unique())), "Your answer must be one of: {}".format(list(hospitals.name.unique()))
        assert submitted=="JAMAICA HOSPITAL MEDICAL CENTER", "Try again."
        
class Q6(CodingProblem):
    _var = "new_percentage"
    _hint = ("Fill in locations corresponding to two relatively warmer areas of the heatmap.")
    _solution = CS(
"""# Proposed location of hospital 1
lat_1 = 40.6714
long_1 = -73.8492

# Proposed location of hospital 2
lat_2 = 40.6702
long_2 = -73.7612
""")
    def check(self, submitted):
        assert submitted < 10, \
        ("Your answer will be marked correct, once you choose two hospital locations that bring the "
         "percentage from step 3 below 10%. Unfortunately, your calculated percentage is currently "
         "{}%. Please use the map to find two new hospital locations.").format(submitted)

qvars = bind_exercises(globals(), [
    Q1, Q2, Q3, Q4, Q5, Q6
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
