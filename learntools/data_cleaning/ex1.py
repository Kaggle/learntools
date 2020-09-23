import pandas as pd
import numpy as np

from learntools.core import *

sf_permits = pd.read_csv("../input/building-permit-applications-data/Building_Permits.csv")
np.random.seed(0) 

missing_values_count = sf_permits.isnull().sum()
total_cells = np.product(sf_permits.shape)
total_missing = missing_values_count.sum()
percent_missing = (total_missing/total_cells) * 100

sf_permits_with_na_dropped = sf_permits.dropna(axis=1)

cols_in_original_dataset = sf_permits.shape[1]
cols_in_na_dropped = sf_permits_with_na_dropped.shape[1]
dropped_columns = cols_in_original_dataset - cols_in_na_dropped

class TakeFirstLook(ThoughtExperiment):
    _hint = "Use `sf_permits.head()` to view the first five rows of the data."
    _solution = ('The first five rows of the data does show that several columns have '
                 'missing values.  You can see this in the "Street Number Suffix", "Proposed Construction Type" ' 
                 'and "Site Permit" columns, among others.')
    
class PercentMissingValues(EqualityCheckProblem):
    _var = 'percent_missing'
    _expected = percent_missing
    _hint = ("You can begin by getting the number of missing entries in each column "
             "with `missing_values_count = sf_permits.isnull().sum()`.")
    _solution = CS(
"""# get the number of missing data points per column
missing_values_count = sf_permits.isnull().sum()

# how many total missing values do we have?
total_cells = np.product(sf_permits.shape)
total_missing = missing_values_count.sum()

# percent of data that is missing
percent_missing = (total_missing/total_cells) * 100
""")

class WhyDataMissing(ThoughtExperiment):
    _hint = ("Do all addresses generally have a street number suffix?  Do all addresses generally have a zipcode?")
    _solution = ('If a value in the "Street Number Suffix" column is missing, it is likely because it does not exist. '
                 'If a value in the "Zipcode" column is missing, it was not recorded.')
        
class DropMissingRows(ThoughtExperiment):
    _hint = ("Use `sf_permits.dropna()` to drop all missing rows.")
    _solution = ("There are no rows remaining in the dataset!")
             
class DropMissingCols(EqualityCheckProblem):
    _vars = ['sf_permits_with_na_dropped', 'dropped_columns']
    _expected = [sf_permits_with_na_dropped, dropped_columns]
    _hint = ("You can begin by getting the dropping all columns with missing values "
             "with `sf_permits.dropna(axis=1)`.")
    _solution = CS(
"""# remove all columns with at least one missing value
sf_permits_with_na_dropped = sf_permits.dropna(axis=1)

# calculate number of dropped columns
cols_in_original_dataset = sf_permits.shape[1]
cols_in_na_dropped = sf_permits_with_na_dropped.shape[1]
dropped_columns = cols_in_original_dataset - cols_in_na_dropped
""")
    
class ImputeAutomatically(EqualityCheckProblem):
    _var = 'sf_permits_with_na_imputed'
    _expected = sf_permits.fillna(method='bfill', axis=0).fillna(0)
    _hint = ("Use the `.fillna()` method twice.")
    _solution = CS(
"""sf_permits_with_na_imputed = sf_permits.fillna(method='bfill', axis=0).fillna(0)
""")
               
qvars = bind_exercises(globals(), [
    TakeFirstLook,
    PercentMissingValues,
    WhyDataMissing,
    DropMissingRows,
    DropMissingCols,
    ImputeAutomatically
    ],
    var_format='q{n}',
    )
__all__ = list(qvars)
