from numpy import random
import pandas as pd

from learntools.core.utils import bind_exercises
from learntools.core.problem_factories import simple_problem
from learntools.core.richtext import CodeSolution as CS
from learntools.core.problem import *


class WhichEffectLargerRange(EqualityCheckProblem):
    _var = 'feature_with_bigger_range_of_effects'
    _expected = 'diag_1_428'
    _solution = CS(
"""
# the range of diag_1_428 is wider, largely due to the few points on the far right.
feature_with_bigger_range_of_effects = 'diag_1_428'
""")

class IsEffectRangeImportance(ThoughtExperiment):
    _solution =
"""
No. The width of the effects range is not a reasonable approximation to permutation importance. For that matter, the width of the range doesn't map well to any intuitive sense of "importance" because it can be determined by just a few outliers.
However if all dots on the graph are widely spread from each other, that is a reasonable indication that permutation importance is high.
"""

class CompareEffectSizeWhenChanged(EqualityCheckProblem):
    _var = 'bigger_effect_when_changed'
    _expected = 'diag_1_428'
    _solution =
"""
While most SHAP values of diag_1_428 are small, the few pink dots (high values of the variable, corresponding to people with that diagnosis) have large SHAP values.  In other words, the pink dots for this variable are far from 0, and making someone have the higher (pink) value would increase their readmission risk significantly.
In real-world terms, this diagnosis is rare, but poses a larger risk for people who have it.
In contrast, `payer_code_?` has many values of both blue and pink, and both have SHAP values that differ meaningfully from 0.
But changing `payer_code_?` from 0 (blue) to 1 (pink) is likely to have a smaller impact than changing `diag_1_428`.
""")


qvars = bind_exercises(globals(), [
    WhichEffectLargerRange,
    IsEffectRangeImportance,
    CompareEffectSizeWhenChanged
    ],
    tutorial_id=FILLTHISIN,
    var_format='q_{n}',
    )
__all__ = list(qvars)
