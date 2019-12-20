import datetime
from decimal import Decimal
import pandas as pd
import numpy as np

from learntools.core import *

class WhyThatUShape(ThoughtExperiment):
    _solution = \
"""
The code is

    for feat_name in base_features:
        pdp_dist = pdp.pdp_isolate(model=first_model, dataset=val_X,
                                   model_features=base_features, feature=feat_name)
        pdp.pdp_plot(pdp_dist, feat_name)
        plt.show()


We have a sense from the permutation importance results that distance is the most important determinant of taxi fare.

This model didn't include distance measures (like absolute change in latitude or longitude) as features, so coordinate features (like `pickup_longitude`) capture the effect of distance.
Being picked up near the center of the longitude values lowers predicted fares on average, because it means shorter trips (on average).

For the same reason, we see the general U-shape in all our partial dependence plots.
"""

class PonderPDPContour(ThoughtExperiment):
    _solution = \
"""
You should expect the plot to have contours running along a diagonal. We see that to some extent, though there are interesting caveats.

We expect the diagonal contours because these are pairs of values where the pickup and dropoff longitudes are nearby, indicating shorter trips (controlling for other factors).

As you get further from the central diagonal, we should expect prices to increase as the distances between the pickup and dropoff longitudes also increase.

The surprising feature is that prices increase as you go further to the upper-right of this graph, even staying near that 45-degree line.

This could be worth further investigation, though the effect of moving to the upper right of this graph is small compared to moving away from that 45-degree line.

The code you need to create the desired plot is:

    fnames = ['pickup_longitude', 'dropoff_longitude']
    longitudes_partial_plot  =  pdp.pdp_interact(model=first_model, dataset=val_X,
                                                model_features=base_features, features=fnames)
    pdp.pdp_interact_plot(pdp_interact_out=longitudes_partial_plot,
                          feature_names=fnames, plot_type='contour')
    plt.show()
"""

class ReadPDPContour(CodingProblem):
    _var = 'savings_from_shorter_trip'
    _hint = 'First find the vertical level corresponding to -74 dropoff longitude. Then read off the horizontal values you are switching between. Use the white contour lines to orient yourself on what values you are near. You can round to the nearest integer rather than stressing about the exact cost to the nearest penny'
    _solution = 'About \$15. The price decreases from slightly more than \$24 to slightly more than \$9.'
    def check(self, savings):
        if type(savings) == str:
            savings = Decimal(dollars.strip('$'))
        assert ((savings > 13) and (savings < 17)), "Your answer should be about 15. Not {}".format(savings)

class MakePDPWithAbsFeatures(CodingProblem):
    _var = 'pdp_dist'
    _hint = 'use the abs function when creating the abs_lat_change and abs_lon_change features. You don\'t need to change anything else.'
    _solution = \
"""
The biggest difference is that the partial dependence plot became much smaller. The the lowest vertical value is about $15 below the highest vertical value in the top chart, whereas this difference is only about $3 in the chart you just created. In other words, once you control for absolute distance traveled, the pickup_longitude has only a very small impact on predictions.

    # create new features
    data['abs_lon_change'] = abs(data.dropoff_longitude - data.pickup_longitude)
    data['abs_lat_change'] = abs(data.dropoff_latitude - data.pickup_latitude)
"""

    def check(self, pdp_result):
        correct = np.array([9.92212681,  8.97384862,  8.80044327,  8.71024292,  8.71564739,
                         8.73523192,  8.76626448,  8.87855912,  9.00098688, 10.99584622])
        submitted = pdp_result.pdp
        assert np.allclose(submitted, correct, rtol=0.1)

class DoesSteepnessImplyImportance(ThoughtExperiment):
    _solution = "No. This doesn't guarantee `feat_a` is more important. For example, `feat_a` could have a big effect in the cases where it varies, but could have a single value 99\% of the time. In that case, permuting `feat_a` wouldn't matter much, since most values would be unchanged."

class DesignDatasetUShapedPdp(CodingProblem):
    _var = 'pdp_dist'
    _hint = "Consider explicitly using terms that include mathematical expressions like `(X1 < -1)`"
    _solution = CS(
"""
# There are many possible solutions.
# One example expression for y is.
y = -2 * X1 * (X1<-1) + X1 - 2 * X1 * (X1>1) - X2
# You don't need any more changes
""")

    def check(self, pdp_result):
        segment_1_end = np.argmin(pdp_result.feature_grids<-1)
        segment_3_start = np.argmax(pdp_result.feature_grids>1)
        segment_2_start = segment_1_end + 1
        segment_2_end = segment_3_start - 1

        segment_1_slopes_down = pdp_result.pdp[0] > pdp_result.pdp[segment_1_end]
        segment_2_slopes_up = pdp_result.pdp[segment_2_start] < pdp_result.pdp[segment_2_end]
        segment_3_slopes_down = pdp_result.pdp[segment_3_start] > pdp_result.pdp[-1]

        assert segment_1_slopes_down, ("The partial dependence plot does not slope down for values below -1.")
        assert segment_2_slopes_up, ("The partial dependence plot does not slope up for values between -1 and 1.")
        assert segment_3_slopes_down, ("The partial dependence plot does not slope down for values above 1.")

class DesignFlatPDPWithHighImportance(CodingProblem):
    _vars = ['perm', 'pdp_dist']
    _hint = "You need for X1 to affect the prediction in order to have it affect permutation importance. But the average effect needs to be 0 to satisfy the PDP requirement. Achieve this by creating an interaction, so the effect of X1 depends on the value of X2 and vice-versa."
    _solution = CS(
"""
# Create array holding predictive feature
X1 = 4 * rand(n_samples) - 2
X2 = 4 * rand(n_samples) - 2
# Create y. you should have X in the expression for y
y = X1 * X2

# Aside from these lines, use the code provided
""")

    def check(self, importance, pdpResult):
        X1_imp = importance.feature_importances_[0]
        pdpRange = max(pdpResult.pdp) - min(pdpResult.pdp)
        assert (X1_imp > 0.5), ("Tested that X1 has an importance > 0.5. "
                                "Actual importance was {}").format(X1_imp)
        assert (pdpRange < 0.5), ("Tested that the highest point on the Partial "
                                  "Dependence Plot is within 0.5 of the lowest point. "
                                  "Actual difference was {}").format(pdpRange)


qvars = bind_exercises(globals(), [
    WhyThatUShape,
    PonderPDPContour,
    ReadPDPContour,
    MakePDPWithAbsFeatures,
    DoesSteepnessImplyImportance,
    DesignDatasetUShapedPdp,
    DesignFlatPDPWithHighImportance
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
