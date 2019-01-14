from learntools.core import *


class GetTableName(EqualityCheckProblem):
    _var = 'table_name'
    _expected = 'taxi_trips'
    _solution = CS("""
# Find the table name with the following command
chicago_taxi_helper.list_tables()

table_name = 'taxi_trips'
    """)

class WhatsWrongWithData(ThoughtExperiment):
    _solution = \
"""
You can see the data by calling `chicago_taxi_trips.head('taxi_trips')`.  

Some trips the top few rows have `trip_seconds` or `trip_miles` values of 0. 
Other location fields have values of `None`. That is a problem if we want to use those fields.
"""


class YearDistrib(CodingProblem):
    _var = 'rides_per_year_result'
    def check(self, results):
        results.columns = [c.lower() for c in results.columns]
        assert ('year' in results.columns), ('Your results hould have a `year` column. But your columns are {}'.format(list(results.columns)))
        assert (2013 in results.year.values), ('Your year columns did not have the value 2013. That should be in there')
        first_year_rides = results.query('year == 2013').num_trips[0]
        assert (first_year_rides == 26870287), ('There should have been 26870287 rides in 2013. But your results showed {}'.format(first_year_rides))

    _hint = "Start your query with  `SELECT EXTRACT(YEAR FROM trip_start_timestamp) AS year, COUNT(1) num_trips`"
    _solution = CS(
"""
rides_per_year_query = \"""SELECT EXTRACT(YEAR FROM trip_start_timestamp) AS year, COUNT(1) num_trips
                    from `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                    GROUP BY year
                    ORDER BY year\"""

rides_per_year_result = chicago_taxi_helper.query_to_pandas_safe(rides_per_year_query)
"""
)

class MonthDistrib(CodingProblem):
    _var = 'rides_per_month_result'
    def check(self, results):
        results.columns = [c.lower() for c in results.columns]
        assert ('month' in results.columns), ('Your results hould have a `month` column. But your columns are {}'.format(list(results.columns)))
        assert (1 in results.month), ('Your month columns did not have the value 1 in it. That should be in there')
        jan_rides = results.query('month==1').num_trips[0]
        assert (jan_rides == 1040262), ('There should have been 1040262 rides in January. But your results showed {}'.format(jan_rides))

    _hint = "Start your query with  `SELECT EXTRACT(MONTH FROM trip_start_timestamp) AS month, COUNT(1) num_trips`"
    _solution = CS(
"""
rides_per_month_query = \"""SELECT EXTRACT(MONTH FROM trip_start_timestamp) AS month, COUNT(1) num_trips
                    from `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                    WHERE EXTRACT(YEAR FROM trip_start_timestamp) = 2017
                    GROUP BY month
                    ORDER BY month\"""

rides_per_month_result = chicago_taxi_helper.query_to_pandas_safe(rides_per_month_query)
"""
)

class TheLongQuery(CodingProblem):
    _var = 'speeds_result'
    def check(self, results):
        results.columns = [c.lower() for c in results.columns]
        assert('hour_of_day' in results.columns), ("Your results should have an `hour_of_day` column")
        assert('num_trips' in results.columns), ("Your results should have an `num_trips` column")
        assert('avg_mph' in results.columns), ("Your results should have an `avg_mph` column")
        assert(results.shape[0] == 12), ('Should have 12 rows in your results but have {}'.format(results.shape[0]))
        first_hour_num_trips = results.query('hour_of_day == 1').num_trips[0]
        assert(first_hour_num_trips != 526723), ('You got most of the query right, but forgot to remove rides with `trip_seconds` or `trip_miles` of 0.')
        assert(first_hour_num_trips == 427383), ('Hour 1 should have 427383 trips but you have {}'.format(first_hour_num_trips))

    _solution = CS(
"""
speeds_query = \"""WITH RelevantRides AS
(SELECT EXTRACT(HOUR FROM trip_start_timestamp) hour_of_day, trip_miles, trip_seconds
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE trip_start_timestamp > '2017-01-01' and trip_start_timestamp < '2017-07-01'
    AND trip_seconds > 0 AND trip_miles > 0
)

SELECT hour_of_day, count(1) num_trips, 3600 * SUM(trip_miles) / SUM(trip_seconds) avg_mph
FROM RelevantRides
GROUP BY hour_of_day
ORDER BY hour_of_day\"""

speeds_result = chicago_taxi_helper.query_to_pandas_safe(speeds_query, max_gb_scanned=20)
"""
)

class AllRidesInTheMorning(ThoughtExperiment):
    _solution = \
"""
The results show rides with hours 1-12. But there should results in the afternoon (hours 13-24).

Perhaps the raw data has lost the distinction between AM and PM values.

You can review 200 rows of the raw data with the command `chicago_taxi_trips.head('taxi_trips', num_rows=200)`

You'll see that the timestamps are all in the AM hours (hours are less than or equal to 12.) 

At first you might worry that the data is coming back sorted by time, but the variety of dates suggests that's not the case. 
Part of data science is tracking down exactly this type of problem. If you were in an organization working on this, you could show the evidence you've just collected (e.g. the breakdown of trips by hour) to someone responsible for collecting the data, and help them debug the data collection and storage process using the results you've collected.
"""


qvars = bind_exercises(globals(), [
    GetTableName,
    WhatsWrongWithData,
    YearDistrib,
    MonthDistrib,
    TheLongQuery,
    AllRidesInTheMorning
    ],
    tutorial_id=81,
    var_format='q_{n}',
    )

__all__ = list(qvars)
