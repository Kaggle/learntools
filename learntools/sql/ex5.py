from learntools.core import *


class GetTableName(EqualityCheckProblem):
    _var = 'table_name'
    _expected = 'taxi_trips'
    _solution = CS("""
# List all the tables in the dataset
tables = list(client.list_tables(dataset))

# Print names of all tables in the dataset (there is only one!)
for table in tables:  
    print(table.table_id)

table_name = 'taxi_trips'
    """)

class WhatsWrongWithData(ThoughtExperiment):
    _solution = \
"""
You can see the data by calling: 
```python
# Construct a reference to the "taxi_trips" table
table_ref = dataset_ref.table("taxi_trips")

# API request - fetch the table
table = client.get_table(table_ref)

# Preview the first five lines of the "taxi_trips" table
client.list_rows(table, max_results=5).to_dataframe()
```

Some trips in the top few rows have `trip_seconds` or `trip_miles` values of 0. 
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

    _hint = "Start your query with  `SELECT EXTRACT(YEAR FROM trip_start_timestamp) AS year, COUNT(1) AS num_trips`"
    _solution = CS(
"""
rides_per_year_query = \"""
                       SELECT EXTRACT(YEAR FROM trip_start_timestamp) AS year, 
                              COUNT(1) AS num_trips
                       FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                       GROUP BY year
                       ORDER BY year
                       \"""

# Set up the query
rides_per_year_query_job = client.query(rides_per_year_query)

# API request - run the query, and return a pandas DataFrame
rides_per_year_result = rides_per_year_query_job.to_dataframe()
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

    _hint = "Start your query with `SELECT EXTRACT(MONTH FROM trip_start_timestamp) AS month, COUNT(1) AS num_trips`"
    _solution = CS(
"""
rides_per_month_query = \"""
                        SELECT EXTRACT(MONTH FROM trip_start_timestamp) AS month, 
                               COUNT(1) AS num_trips
                        FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                        WHERE EXTRACT(YEAR FROM trip_start_timestamp) = 2017
                        GROUP BY month
                        ORDER BY month
                        \"""

# Set up the query
rides_per_month_query_job = client.query(rides_per_month_query)

# API request - run the query, and return a pandas DataFrame
rides_per_month_result = rides_per_month_query_job.to_dataframe()
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
speeds_query = \"""
               WITH RelevantRides AS
               (
                   SELECT EXTRACT(HOUR FROM trip_start_timestamp) AS hour_of_day, 
                          trip_miles, 
                          trip_seconds
                   FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                   WHERE trip_start_timestamp > '2017-01-01' AND 
                         trip_start_timestamp < '2017-07-01' AND 
                         trip_seconds > 0 AND 
                         trip_miles > 0
               )
               SELECT hour_of_day, 
                      COUNT(1) AS num_trips, 
                      3600 * SUM(trip_miles) / SUM(trip_seconds) AS avg_mph
               FROM RelevantRides
               GROUP BY hour_of_day
               ORDER BY hour_of_day
               \"""

# Set up the query
speeds_query_job = client.query(speeds_query)

# API request - run the query, and return a pandas DataFrame
speeds_result = speeds_query_job.to_dataframe()

# View results
print(speeds_result)
"""
)

class AllRidesInTheMorning(ThoughtExperiment):
    _solution = \
"""
The results show rides with hours 1-12. But there should results in the afternoon (hours 13-24).

Perhaps the raw data has lost the distinction between AM and PM values.

You can review 200 rows of the raw data with the commands: 
```python
# Construct a reference to the "taxi_trips" table
table_ref = dataset_ref.table("taxi_trips")

# API request - fetch the table
table = client.get_table(table_ref)

# Preview the first five lines of the "taxi_trips" table
client.list_rows(table, max_results=200).to_dataframe()
```

You'll see that the timestamps are all in the AM hours (hours are less than or equal to 12.) 

At first you might worry that the data is coming back sorted by time, but the variety of dates suggests that's not the case. 
Part of data science is tracking down exactly this type of problem. If you were in an organization working on this, you could show the evidence you've just collected (e.g. the breakdown of trips by hour) to someone responsible for collecting the data, and help them debug the data collection and storage process.
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
