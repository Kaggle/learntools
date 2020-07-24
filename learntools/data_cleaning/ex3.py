from learntools.core import *

import pandas as pd
import numpy as np
import seaborn as sns
import datetime

earthquakes = pd.read_csv("../input/earthquake-database/database.csv")
np.random.seed(0)
earthquakes.loc[3378, "Date"] = "02/23/1975"
earthquakes.loc[7512, "Date"] = "04/28/1985"
earthquakes.loc[20650, "Date"] = "03/13/2011"
earthquakes['date_parsed'] = pd.to_datetime(earthquakes['Date'], format="%m/%d/%Y")

day_of_month_earthquakes = earthquakes['date_parsed'].dt.day

class CheckDtype(ThoughtExperiment):
    _hint = ('Use `earthquakes[\'Date\'].head()` to check that the column contains dates and verify that it has '
             'dtype "object".  You can also use `earthquakes[\'Date\'].dtype` to verify the dtype.')
    _solution = ('The "Date" column in the `earthquakes` DataFrame does have dates.  The dtype is "object".')
    
class ConvertToDatetime(CodingProblem):
    _var = 'earthquakes'
    _hint = ("Since there are only three rows with a fancy type, you might consider manually editing them. "
             "For instance, you can begin by setting `earthquakes.loc[3378, \"Date\"] = \"02/23/1975\"`.")
    _solution = CS(
"""
earthquakes.loc[3378, "Date"] = "02/23/1975"
earthquakes.loc[7512, "Date"] = "04/28/1985"
earthquakes.loc[20650, "Date"] = "03/13/2011"
earthquakes['date_parsed'] = pd.to_datetime(earthquakes['Date'], format="%m/%d/%Y")
""")
    def check(self, earthquakes_to_check):
        assert type(earthquakes_to_check) == pd.core.frame.DataFrame, "`earthquakes` is not a DataFrame."
        assert len(earthquakes_to_check) == len(earthquakes), "`earthquakes` should have {} rows, but it has {} rows.".format(len(earthquakes), len(earthquakes_to_check))
        assert 'date_parsed' in earthquakes_to_check.columns, "'date_parsed' is not a column in `earthquakes`."
        assert earthquakes_to_check['date_parsed'].dtype != 'object', "The 'date_parsed' column does not have correctly parsed dates.  It still has dtype 'object'."
        assert earthquakes_to_check['date_parsed'].dt.day.loc[0]==2, "Something doesn't look right."

class DayOfMonth(EqualityCheckProblem):
    _var = 'day_of_month_earthquakes'
    _expected = day_of_month_earthquakes
    _hint = "Use the `.dt` accessor."
    _solution = CS(
"""day_of_month_earthquakes = earthquakes['date_parsed'].dt.day
""")
        
class PlotDayOfMonth(ThoughtExperiment):
    _hint = """
Remove the missing values, and then use `sns.distplot()` as follows:

```python
# remove na's
day_of_month_earthquakes = day_of_month_earthquakes.dropna()

# plot the day of the month
sns.distplot(day_of_month_earthquakes, kde=False, bins=31)
```

"""
    _solution = ("The graph should make sense: it shows a relatively even distribution in days of the month,"
                 "which is what we would expect.")
               
qvars = bind_exercises(globals(), [
    CheckDtype,
    ConvertToDatetime,
    DayOfMonth,
    PlotDayOfMonth
    ],
    var_format='q{n}',
    )
__all__ = list(qvars)
