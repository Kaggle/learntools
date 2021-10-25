from learntools.core import *

import math
import pandas as pd
import geopandas as gpd
from learntools.geospatial.tools import Nominatim

congrats_map_completion = "Thank you for creating a map!"
correct_message_map_completion = ""

def check_gdf_equal(gdf1, gdf2):
    df1 = pd.DataFrame(gdf1.drop(columns='geometry'))
    df2 = pd.DataFrame(gdf2.drop(columns='geometry'))
    assert df1.equals(df2), "The results don't look right.  Try again."
    geom1 = gdf1.geometry
    geom2 = gdf2.geometry
    assert geom1.equals(geom2), "The results don't look right.  Try again."

# Q1
starbucks = pd.read_csv("../input/geospatial-learn-course-data/starbucks_locations.csv")
rows_with_missing = starbucks[starbucks["City"]=="Berkeley"]
geolocator = Nominatim(user_agent="kaggle_learn")
def my_geocoder(row):
    point = geolocator.geocode(row).point
    return pd.Series({'Latitude': point.latitude, 'Longitude': point.longitude})
berkeley_locations = rows_with_missing.apply(lambda x: my_geocoder(x['Address']), axis=1)
starbucks.update(berkeley_locations)

# Q3
CA_counties = gpd.read_file("../input/geospatial-learn-course-data/CA_county_boundaries/CA_county_boundaries/CA_county_boundaries.shp")
CA_pop = pd.read_csv("../input/geospatial-learn-course-data/CA_county_population.csv", index_col="GEOID")
CA_high_earners = pd.read_csv("../input/geospatial-learn-course-data/CA_county_high_earners.csv", index_col="GEOID")
CA_median_age = pd.read_csv("../input/geospatial-learn-course-data/CA_county_median_age.csv", index_col="GEOID")
cols_to_add = CA_pop.join([CA_high_earners, CA_median_age]).reset_index()
CA_stats = CA_counties.merge(cols_to_add, on="GEOID")

class Q1(CodingProblem):
    _var = 'starbucks'
    _hint = ("Use `geolocator.geocode()` to get the missing locations from the addresses in the "
             "\"Address\" column.  You might find the [`pd.DataFrame.update()`](https://bit.ly/2kEyXP9l) "
             "method useful to solve this problem.")
    _solution = CS(
"""def my_geocoder(row):
    point = geolocator.geocode(row).point
    return pd.Series({'Latitude': point.latitude, 'Longitude': point.longitude})

berkeley_locations = rows_with_missing.apply(lambda x: my_geocoder(x['Address']), axis=1)
starbucks.update(berkeley_locations)
""")
    def check(self, submitted_starbucks):
        # missing entries filled in?
        num_missing = submitted_starbucks.isna().sum().sum()
        assert num_missing==0, "The `starbucks` DataFrame still has {} missing entries.  Please fill in these values.".format(num_missing)
        
        # only berkeley addresses changed
        not_berkeley = starbucks[~(starbucks["City"]=="Berkeley")]
        assert submitted_starbucks[~(submitted_starbucks["City"]=="Berkeley")].equals(not_berkeley), \
        "Please only amend the rows for Starbucks locations in Berkeley.  All other rows should be left as-is."
        
        # didn't change columns
        assert set(starbucks.columns) == set(submitted_starbucks.columns), \
        "Please only fill in the missing values in the `starbucks` DataFrame.  Do not add or remove columns."                     
        # dataframes equal?
        assert starbucks.equals(submitted_starbucks), "Did you use the nominatim geocoder to fill in the values?"

class Q2P(CodingProblem):
    _hint = "Use `folium.Marker()` to add a location for each entry in `starbucks[starbucks[\"City\"]=='Berkeley']`."
    _solution = CS(
"""# Add a marker for each Berkeley location
for idx, row in starbucks[starbucks["City"]=='Berkeley'].iterrows():
    Marker([row['Latitude'], row['Longitude']]).add_to(m_2)
""")
    _congrats = congrats_map_completion
    _correct_message = correct_message_map_completion
    def check(self):
        pass 
    
class Q2T(ThoughtExperiment):
    _hint = "Use the map above to answer the question."
    _solution = "All five locations appear to be correct!"

Q2 = MultipartProblem(Q2P, Q2T)


class Q3(CodingProblem):
    _var = "CA_stats"
    _hint = ("Begin by using [`pd.DataFrame.join()`](https://www.kaggle.com/residentmario/renaming-and-combining)"
             "to join the three DataFrames together.  Then, add this new DataFrame to the `CA_counties`"
             "GeoDataFrame with `gpd.GeoDataFrame.merge()`.")
    _solution = CS(
"""cols_to_add = CA_pop.join([CA_high_earners, CA_median_age]).reset_index()
CA_stats = CA_counties.merge(cols_to_add, on="GEOID")
""")
    def check(self, results):
        assert set(CA_stats.columns)==set(results.columns), "The columns don't look right.  They should be {}, but your columns were {}".format(list(CA_stats.columns), list(results.columns))
        assert '4326' in results.crs.to_string(), \
        ("Please set the CRS of `CA_stats` to EPSG 4326 by running "
         "`CA_stats.crs = {'init': 'epsg:4326'}`.")
        assert len(CA_stats)==len(results), \
        "`CA_stats` should have {} rows.  But, it has {}.".format(len(CA_stats), len(results))
        
        my_cols = list(CA_stats.columns)
        soln = CA_stats.loc[:, my_cols].sort_values("GEOID")
        to_check = results.loc[:, my_cols].sort_values("GEOID")
        check_gdf_equal(to_check, soln)

class Q4(CodingProblem):
    _var = "sel_counties"
    _hint = "Review conditional selection [here](https://www.kaggle.com/residentmario/indexing-selecting-assigning/)."
    _solution = CS(
"""sel_counties = CA_stats[((CA_stats.high_earners > 100000) &
                         (CA_stats.median_age < 38.5) &
                         (CA_stats.density > 285) &
                         ((CA_stats.median_age < 35.5) |
                         (CA_stats.density > 1400) |
                         (CA_stats.high_earners > 500000)))]
""")
    def check(self, results):
        CA_stats["density"] = CA_stats["population"] / CA_stats["area_sqkm"]
        sel_counties = CA_stats[((CA_stats.high_earners > 100000) & \
                         (CA_stats.median_age < 38.5) & \
                         (CA_stats.density > 285) & \
                       ((CA_stats.median_age < 35.5) | \
                         (CA_stats.density > 1400) | \
                         (CA_stats.high_earners > 500000)))]
        assert(len(sel_counties)==len(results)), \
        "`sel_counties` should have {} rows, but it has {}".format(len(sel_counties), len(results))
        assert set(sel_counties.GEOID) == set(results.GEOID), \
        "You have selected the wrong counties."

class Q5(CodingProblem):
    _var = "num_stores"
    _hint = ("Use a spatial join with `starbucks_gdf` and `sel_counties`.")
    _solution = CS(
"""locations_of_interest = gpd.sjoin(starbucks_gdf, sel_counties)
num_stores = len(locations_of_interest)
""")
    def check(self, num_stores):
        assert type(num_stores)==int, "Your answer should be an integer."
        assert num_stores == 1043, "Please try again."
        
class Q6(CodingProblem):
    _hint = ("We visualized store locations with `folium.plugins.MarkerCluster()`.")
    _solution = CS(
"""# Show selected store locations
mc = MarkerCluster()

locations_of_interest = gpd.sjoin(starbucks_gdf, sel_counties)
for idx, row in locations_of_interest.iterrows():
    if not math.isnan(row['Longitude']) and not math.isnan(row['Latitude']):
        mc.add_child(folium.Marker([row['Latitude'], row['Longitude']]))
        
m_6.add_child(mc)
""")
    _congrats = congrats_map_completion
    _correct_message = correct_message_map_completion
    def check(self):
        pass
        
        
qvars = bind_exercises(globals(), [
    Q1, Q2, Q3, Q4, Q5, Q6
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
