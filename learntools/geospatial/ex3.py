from learntools.core import *

congrats_map_completion = "Thank you for creating a map!"
correct_message_map_completion = ""

class Q1P(CodingProblem):
    _hint = ("Use `folium.plugins.HeatMap()` to add a heatmap. Set `data` to a DataFrame containing the latitude "
        "and longitude locations.  We got fairly good results by setting `radius=15`. Don't forget "
        "to add it to the map with the `add_to()` method!")
    _solution = CS(
"""# Add a heatmap to the map
HeatMap(data=earthquakes[['Latitude', 'Longitude']], radius=15).add_to(m_1)
""")
    _congrats = congrats_map_completion
    _correct_message = correct_message_map_completion
    def check(self):
        pass

class Q1T(ThoughtExperiment):
    _hint = "Use the map above to answer the question."
    _solution = "Yes, earthquakes coincide with plate boundaries."

Q1 = MultipartProblem(Q1P, Q1T)

class Q2P(CodingProblem):
    _hint = ("Use `folium.Circle()` to create a bubble map. We visualized the relationship between location and "
        "depth by assigning the color of each circle based on the depth of the corresponding earthquake.")
    _solution = CS(
"""# Custom function to assign a color to each circle
def color_producer(val):
    if val < 50:
        return 'forestgreen'
    elif val < 100:
        return 'darkorange'
    else:
        return 'darkred'

# Add a map to visualize earthquake depth
for i in range(0,len(earthquakes)):
    folium.Circle(
        location=[earthquakes.iloc[i]['Latitude'], earthquakes.iloc[i]['Longitude']],
        radius=2000,
        color=color_producer(earthquakes.iloc[i]['Depth'])).add_to(m_2)
""")
    _congrats = congrats_map_completion
    _correct_message = correct_message_map_completion
    def check(self):
        pass 

class Q2T(ThoughtExperiment):
    _hint = "Use the map above to answer the question."
    _solution = ("In the northern half of Japan, it does appear that earthquakes closer to plate boundaries "
    "tend to be shallower (and earthquakes farther from plate boundaries are deeper).  This pattern is "
    "repeated in other locations, such as the western coast of South America.  But, it does not hold "
    "everywhere (for instance, in China, Mongolia, and Russia).")

Q2 = MultipartProblem(Q2P, Q2T)

class Q3P(CodingProblem):
    _hint = ("Use `folium.Choropleth()` to create a choropleth map.  Remember to use the `__geo_interface__` "
        "method to construct the value for `geo_data`. Set `data` to a Pandas Series containing "
        "the population density data, and indexed by prefecture.")
    _solution = CS(
"""# Create a choropleth map to visualize population density
Choropleth(geo_data=prefectures['geometry'].__geo_interface__,
           data=stats['density'],
           key_on="feature.id",
           fill_color='YlGnBu',
           legend_name='Population density (per square kilometer)'
          ).add_to(m_3)
""")
    _congrats = congrats_map_completion
    _correct_message = correct_message_map_completion
    def check(self):
        pass   

class Q3T(ThoughtExperiment):
    _hint = "Use the map above to answer the question."
    _solution = ("Tokyo, Kanagawa, and Osaka have the highest population density.  All of these prefectures "
        "are located in central Japan, and Tokyo and Kanagawa are adjacent.")

Q3 = MultipartProblem(Q3P, Q3T)

class Q4P(CodingProblem):
    _hint = ("We visualized population density and earthquake magnitude by adding both a choropleth map "
        "and a bubble map to the base map.")
    _solution = CS(
"""# Create a map
def color_producer(magnitude):
    if magnitude > 6.5:
        return 'red'
    else:
        return 'green'

Choropleth(
    geo_data=prefectures['geometry'].__geo_interface__,
    data=stats['density'],
    key_on="feature.id",
    fill_color='BuPu',
    legend_name='Population density (per square kilometer)').add_to(m_4)

for i in range(0,len(earthquakes)):
    folium.Circle(
        location=[earthquakes.iloc[i]['Latitude'], earthquakes.iloc[i]['Longitude']],
        popup=("{} ({})").format(
            earthquakes.iloc[i]['Magnitude'],
            earthquakes.iloc[i]['DateTime'].year),
        radius=earthquakes.iloc[i]['Magnitude']**5.5,
        color=color_producer(earthquakes.iloc[i]['Magnitude'])).add_to(m_4)
""")
    _congrats = congrats_map_completion
    _correct_message = correct_message_map_completion
    def check(self):
        pass    

class Q4T(ThoughtExperiment):
    _hint = "Use the map above to answer the question."
    _solution = ("While there's no clear, single answer to this question, there are a few reasonable "
        "options. **Tokyo** is by far the most densely populated prefecture and has also experienced a number of "
        "earthquakes.  **Osaka** is relatively less densely populated, but experienced an earthquake that was "
        "relatively stronger than those near Tokyo.  And, the long coast of **Kanagawa** (in addition to its high "
        "density and the historical proximity of strong earthquakes) might lead us to worry about the added potential "
        "tsunami risk.")

Q4 = MultipartProblem(Q4P, Q4T)

qvars = bind_exercises(globals(), [
    Q1, Q2, Q3, Q4
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
