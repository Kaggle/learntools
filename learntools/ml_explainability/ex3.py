import datetime
from decimal import Decimal
import pandas as pd
import numpy as np

from learntools.core import *

# 1
class WhyThatUShape(ThoughtExperiment):
    _solution = \
"""
The code is

    for feat_name in base_features:
        PartialDependenceDisplay.from_estimator(first_model, val_X, [feat_name])
        plt.show()


We have a sense from the permutation importance results that distance is the most important determinant of taxi fare.

This model didn't include distance measures (like absolute change in latitude or longitude) as features, so coordinate features (like `pickup_longitude`) capture the effect of distance.
Being picked up near the center of the longitude values lowers predicted fares on average, because it means shorter trips (on average).

For the same reason, we see the general U-shape in all our partial dependence plots.
"""

# 2
class PonderPDPContour(ThoughtExperiment):
    _solution = \
"""
You should expect the plot to have contours running along a diagonal. We see that to some extent, though there are interesting caveats.

We expect the diagonal contours because these are pairs of values where the pickup and dropoff longitudes are nearby, indicating shorter trips (controlling for other factors).

As you get further from the central diagonal, we should expect prices to increase as the distances between the pickup and dropoff longitudes also increase.

The surprising feature is that prices increase as you go further to the upper-right of this graph, even staying near that 45-degree line.

This could be worth further investigation, though the effect of moving to the upper right of this graph is small compared to moving away from that 45-degree line.

The code you need to create the desired plot is:

    fig, ax = plt.subplots(figsize=(8, 6))
    fnames = [('pickup_longitude', 'dropoff_longitude')]
    disp = PartialDependenceDisplay.from_estimator(first_model, val_X, fnames, ax=ax)
    plt.show()
"""

# 3
class ReadPDPContour(CodingProblem):
    _var = 'savings_from_shorter_trip'
    _hint = 'First find the vertical level corresponding to -74 dropoff longitude. Then read off the horizontal values you are switching between. Use the contour lines to orient yourself on what values you are near. You can round to the nearest integer rather than stressing about the exact cost to the nearest penny'
    _solution = 'About 6. The price decreases from slightly less than 15 to slightly less than 9.'
    def check(self, savings):
        if type(savings) == str:
            savings = Decimal(dollars.strip('$'))
        assert ((savings > 4) and (savings < 8)), "Your answer should be about 6. Not {}".format(savings)

# 4
class MakePDPWithAbsFeatures(CodingProblem):
    _var = 'disp'
    _hint = 'Use the abs function when creating the abs_lat_change and abs_lon_change features. You don\'t need to change anything else.'
    _solution = \
"""
The difference is that the partial dependence plot became smaller. Both plots have a lowest vertical value of 8.5.  But, the highest vertical value in the top chart is around 10.7, and the highest vertical value in the bottom chart is below 9.1.  In other words, once you control for absolute distance traveled, the pickup_longitude has a smaller impact on predictions.

    # create new features
    data['abs_lon_change'] = abs(data.dropoff_longitude - data.pickup_longitude)
    data['abs_lat_change'] = abs(data.dropoff_latitude - data.pickup_latitude)
"""
    
    def check(self, disp):
        correct = np.array([8.730515  , 8.73239078, 8.71804165, 8.72179009, 8.93013488,
                            8.68796391, 8.6773792 , 8.6816932 , 8.67547295, 8.64980733,
                            8.64402745, 8.65616918, 8.63485345, 8.60505726, 8.59167824,
                            8.57101857, 8.55601734, 8.55780041, 8.53660205, 8.53548254,
                            8.50739547, 8.50599988, 8.50685068, 8.51981394, 8.52555708,
                            8.50483315, 8.53151955, 8.49615781, 8.49384454, 8.49156773,
                            8.5123399 , 8.47138576, 8.47491902, 8.50240045, 8.50495725,
                            8.50433279, 8.4941558 , 8.50175984, 8.50394946, 8.50890372,
                            8.50606589, 8.48335522, 8.48281078, 8.4730394 , 8.47720942,
                            8.47699659, 8.52118039, 8.50234077, 8.59717268, 8.51092865,
                            8.51177667, 8.51159374, 8.51159432, 8.54379423, 8.50500559,
                            8.50631149, 8.52264825, 8.51989952, 8.52841122, 8.52757692,
                            8.54425047, 8.56425312, 8.56874055, 8.58372296, 8.5589557 ,
                            8.57709991, 8.57441775, 8.59449221, 8.60063777, 8.62185164,
                            8.6155473 , 8.6118143 , 8.61590988, 8.60758597, 8.62013413,
                            8.6334263 , 8.64035478, 8.65324115, 8.66043255, 8.67502176,
                            8.68940416, 8.6840402 , 8.67197893, 8.65512484, 8.66810839,
                            8.6614093 , 8.65865671, 8.66485738, 8.67966737, 8.82833712,
                            9.04135448, 9.03734449, 8.69506545, 8.70261503, 8.70673595,
                            8.69045255, 8.69679997, 8.70716659, 8.71006281, 8.71739009])
        submitted = disp.pd_results[0]['average'][0]
        assert np.allclose(submitted, correct, rtol=0.1)

# 5
class DoesSteepnessImplyImportance(ThoughtExperiment):
    _solution = "No. This doesn't guarantee `feat_a` is more important. For example, `feat_a` could have a big effect in the cases where it varies, but could have a single value 99\% of the time. In that case, permuting `feat_a` wouldn't matter much, since most values would be unchanged."

# 6
class DesignDatasetUShapedPdp(CodingProblem):
    _var = 'disp'
    _hint = "Consider explicitly using terms that include mathematical expressions like `(X1 < -1)`"
    _solution = CS(
"""
# There are many possible solutions.
# One example expression for y is.
y = -2 * X1 * (X1<-1) + X1 - 2 * X1 * (X1>1) - X2
# You don't need any more changes
""")

    def check(self, disp):
        pdp_result = disp.pd_results[0]
        x_values = pdp_result['values'][0]
        y_values = pdp_result['average'][0]
        
        segment_1_end = np.argmin(x_values<-1)
        segment_3_start = np.argmax(x_values>1)
        segment_2_start = segment_1_end + 1
        segment_2_end = segment_3_start - 1

        segment_1_slopes_down = y_values[0] > y_values[segment_1_end]
        segment_2_slopes_up = y_values[segment_2_start] < y_values[segment_2_end]
        segment_3_slopes_down = y_values[segment_3_start] > y_values[-1]

        assert segment_1_slopes_down, ("The partial dependence plot does not slope down for values below -1.")
        assert segment_2_slopes_up, ("The partial dependence plot does not slope up for values between -1 and 1.")
        assert segment_3_slopes_down, ("The partial dependence plot does not slope down for values above 1.")

class DesignFlatPDPWithHighImportance(CodingProblem):
    _vars = ['perm', 'disp']
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

    def check(self, importance, disp):
        X1_imp = importance.feature_importances_[0]
        pdpResult = disp.pd_results[0]['average'][0]
        pdpRange = max(pdpResult) - min(pdpResult)
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
