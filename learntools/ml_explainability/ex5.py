from numpy import random
import pandas as pd

from learntools.core import *


class WhichEffectLargerRange(EqualityCheckProblem):
    _var = 'feature_with_bigger_range_of_effects'
    _expected = 'diag_1_428'
    _solution = CS(
"""
# the range of diag_1_428 is wider, largely due to the few points on the far right.
feature_with_bigger_range_of_effects = 'diag_1_428'
""")

class IsEffectRangeImportance(ThoughtExperiment):
    _solution = \
"""
No. The width of the effects range is not a reasonable approximation to permutation importance. For that matter, the width of the range doesn't map well to any intuitive sense of "importance" because it can be determined by just a few outliers.
However if all dots on the graph are widely spread from each other, that is a reasonable indication that permutation importance is high.
Because the range of effects is so sensitive to outliers, permutation importance is a better measure of what's generally important to the model.
"""

class CompareEffectSizeWhenChanged(EqualityCheckProblem):
    _var = 'bigger_effect_when_changed'
    _expected = 'diag_1_428'
    _solution = \
"""
While most SHAP values of diag_1_428 are small, the few pink dots (high values of the variable, corresponding to people with that diagnosis) have large SHAP values.  In other words, the pink dots for this variable are far from 0, and making someone have the higher (pink) value would increase their readmission risk significantly.
In real-world terms, this diagnosis is rare, but poses a larger risk for people who have it.
In contrast, `payer_code_?` has many values of both blue and pink, and both have SHAP values that differ meaningfully from 0.
But changing `payer_code_?` from 0 (blue) to 1 (pink) is likely to have a smaller impact than changing `diag_1_428`.
"""

class WhyAreShapsValuesJumbled(ThoughtExperiment):
    _solution = \
"""
The jumbling suggests that sometimes increasing that feature leads to higher predictions, and other times it leads to a lower prediction. Said another way, both high and low values of the feature can have both positive and negative effects on the prediction.
The most likely explanation for this "jumbling" of effects is that the variable (in this case `num_lab_procedures`) has an interaction effect with other variables.  For example, there may be some diagnoses for which it is good to have many lab procedures, and other diagnoses where suggests increased risk. We don't yet know what other feature is interacting with `num_lab_procedures` though we could investigate that with SHAP contribution dependence plots.
"""

class WhichWayInteraction(ThoughtExperiment):
    _solution = \
"""
First, recall that the SHAP vaue is an estimate of the impact of a given feature on the prediction. So, if the dots trend from upper left to lower right, that means low values of `feature_of_interest` cause higher predictions.

Returning to this graph:

`feature_of_interest` slopes downward for high values of `other_feature`. To see this, focus your eye on the pink dots (where `other_feature` is high) and imagine a best-fit line through those pink dots.  It slopes down, suggesting that the prediction goes down as `feature_of_interest` increases.

Now focus your eye on the blue dots, and imagine a best fit line through those dots.  It is generally pretty flat, possibly even curving up on the right side of the graph. So increasing `feature_of_interest` has a more positive impact on predictions when `other_feature` is high.
"""

class CompareSHAPDepPlots(ThoughtExperiment):
    _solution = \
"""
Here is the code:

    shap.dependence_plot('num_lab_procedures', shap_values[1], small_val_X)
    shap.dependence_plot('num_medications', shap_values[1], small_val_X)

.
Loosely speaking, **num_lab_procedures** looks like a cloud with little disernible pattern.  It does not slope steeply up nor down at any point. It's hard to say we've learned much from that plot. At the same time, the values are not all very close to 0. So the model seems to think this is a relevant feature. One potential next step would be to explore more by coloring it with different other features to search for an interaction.

On the other hand, **num_medications** clearly slopes up until a value of about 20, and then it turns back down. Without more medical background, this seems a surprising phenomenon... You could do some exploration to see whether these patients have unusual values for other features too. But a good next step would be to discuss this phenomenon with domain experts (in this case, the doctors).
"""

qvars = bind_exercises(globals(), [
    WhichEffectLargerRange,
    IsEffectRangeImportance,
    CompareEffectSizeWhenChanged,
    WhyAreShapsValuesJumbled,
    WhichWayInteraction,
    CompareSHAPDepPlots
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
