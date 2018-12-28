from learntools.core import *


class GetTableName(EqualityCheckProblem):
    pass

class WhatsWrongWithData(ThoughtExperiment):
    pass

class YearDistrib(CodingProblem):
    pass

class MonthDistrib(CodingProblem):
    pass

class TheBigQuery(CodingProblem):
    # NOTE TO SELF: WORKING IN https://www.kaggle.com/dansbecker/fork-of-getting-started-with-sql-and-bigquery-work/edit
    _solution = CS(
"""
WITH RelevantRides AS
(SELECT EXTRACT(HOUR FROM trip_start_timestamp) hour_of_day, trip_miles, trip_seconds
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE trip_start_timestamp > '2017-01-01' and trip_start_timestamp < '2017-07-01'
    AND trip_seconds > 0 AND trip_miles > 0
)

SELECT hour_of_day, count(1) num_trips, 3600 * SUM(trip_miles) / SUM(trip_seconds) avg_mph
FROM RelevantRides
GROUP BY hour_of_day
ORDER BY hour_of_day
"""
)

qvars = bind_exercises(globals(), [
    GetTableName,
    WhatsWrongWithData,
    YearDistrib,
    MonthDistrib,
    TheBigQuery
    ],
    tutorial_id=81,
    var_format='q_{n}',
    )

__all__ = list(qvars)
