from learntools.core import *

class YearPlot(ThoughtExperiment):
    # TODO: *could* make this a checked coding problem, checking the
    # value of c. I'm not sure that really helps though? I think it'll be
    # clear to the user by visual inspection of their results whether or not
    # they've succeeded. (And checking c could lead to false -ves)
    _var = 'c'

    show_solution_on_correct = False

    # TODO: Some commentary on specific patterns of dist. of age?
    _solution = (
"""`c = df.year`

The distribution of year of release does seem to follow some distinct gradients, but the pattern is not global.

Using a colormap that passes through several hues (such as 'brg', or 'cubehelix') can make it easier to identify regions associated with specific eras:

```python
pts = ax.scatter(df.x, df.y, c=c, cmap='cubehelix')
```

Using a qualitative colormap (such as 'Set2') exaggerates this effect even further. 

Simple sequential colormaps that use only one or two colors (e.g. 'Oranges', 'YlGn') are more effective at showing overall patterns from old to new.
""")


class MeanRatingPlot(ThoughtExperiment):

    _hint = 'Our dataframe `df` has a column called "mean_rating" which will be useful here.'
    
    show_solution_on_correct = False

    # Note on relationship between this trend and the year trend we saw previously?
    # Was trend of lots of very old movies in top-right just a manifestation
    # of our tendency to put highly-rated movies at the right?
    _solution = (
"""
```python
fig, ax = plt.subplots(figsize=FS)
c = df.mean_rating
pts = ax.scatter(df.x, df.y, c=c)
cbar = fig.colorbar(pts)
```

Unlike with year of release, there seems to be a clear global pattern here: average rating tends to increase moving from left to right.
""")

class NRatingsPlot(ThoughtExperiment):
    
    # TODO: Mention alternatives like PowerNorm?
    _solution = CS(
"""fig, ax = plt.subplots(figsize=FS)
c = df.n_ratings
pts = ax.scatter(df.x, df.y, c=c, norm=mpl.colors.LogNorm())
cbar = fig.colorbar(pts)
""")

qvars = bind_exercises(globals(), [
    YearPlot,
    MeanRatingPlot,
    NRatingsPlot,
    ],
    var_format='part{n}',
)
__all__ = list(qvars)
