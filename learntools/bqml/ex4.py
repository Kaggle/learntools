import datetime
from decimal import Decimal
import pandas as pd
import numpy as np

from learntools.core import *

class SummarizeModel(ThoughtExperiment):
    _solution = CS(
"""
# Use permutation importance as a succinct model summary
# A measure of model performance on validation data would be useful here too

import eli5
from eli5.sklearn import PermutationImportance

perm = PermutationImportance(my_model, random_state=1).fit(val_X, val_y)
eli5.show_weights(perm, feature_names = val_X.columns.tolist())
"""
    )

class EffectNumInpatient(ThoughtExperiment):
    _solution = CS(
"""
# PDP for number_inpatient feature

from matplotlib import pyplot as plt
from pdpbox import pdp, get_dataset, info_plots

feature_name = 'number_inpatient'
# Create the data that we will plot
my_pdp = pdp.pdp_isolate(model=my_model, dataset=val_X, model_features=val_X.columns, feature=feature_name)

# plot it
pdp.pdp_plot(my_pdp, feature_name)
plt.show()
"""
    )

class EffectTimeInHospital(ThoughtExperiment):
    _solution = \
"""
The results are very different. Specifically time in hospital has a much smaller effect. Code below:

    from matplotlib import pyplot as plt
    from pdpbox import pdp, get_dataset, info_plots

    feature_name = 'time_in_hospital'
    # Create the data that we will plot
    my_pdp = pdp.pdp_isolate(model=my_model, dataset=val_X, model_features=val_X.columns, feature=feature_name)

    # plot it
    pdp.pdp_plot(my_pdp, feature_name)
    plt.show()
"""

class RawActualsInsteadOfPDP(ThoughtExperiment):
    _hint = "This requires a groupby (from pandas) on the raw data, rather than using a model"
    _solution = CS(
"""
# A simple pandas groupby showing the average readmission rate for each time_in_hospital.

# Do concat to keep validation data separate, rather than using all original data
all_train = pd.concat([train_X, train_y], axis=1)

all_train.groupby(['time_in_hospital']).mean().readmitted.plot()
plt.show()
"""
    )

class UseShap(ThoughtExperiment):
    _hint = "Here's the time to use SHAP values"
    _solution = CS(
"""
# Use SHAP values to show the effect of each feature of a given patient

import shap  # package used to calculate Shap values

sample_data_for_prediction = val_X.iloc[0].astype(float)  # to test function

def patient_risk_factors(model, patient_data):
    # Create object that can calculate shap values
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(patient_data)
    shap.initjs()
    return shap.force_plot(explainer.expected_value[1], shap_values[1], patient_data)

"""
)

qvars = bind_exercises(globals(), [
    SummarizeModel,
    EffectNumInpatient,
    EffectTimeInHospital,
    RawActualsInsteadOfPDP,
    UseShap
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
