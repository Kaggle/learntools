import math
import pandas as pd
from google.cloud import bigquery
from IPython.display import display

from learntools.core import *

# Setup 
client = bigquery.Client()

# (1) TaxiDemand
avg_num_trips_query = """
                      WITH trips_by_day AS
                      (
                      SELECT DATE(trip_start_timestamp) AS trip_date,
                          COUNT(*) as num_trips
                      FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                      WHERE trip_start_timestamp > '2016-01-01' AND trip_start_timestamp < '2016-04-01'
                      GROUP BY trip_date
                      )
                      SELECT trip_date,
                          AVG(num_trips) 
                          OVER (
                               ORDER BY trip_date
                               ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING
                               ) AS avg_num_trips
                      FROM trips_by_day
                      """
avg_num_trips_answer = client.query(avg_num_trips_query).result().to_dataframe()

# (2) CommunityArea
trip_number_query = """
                    SELECT pickup_community_area,
                        trip_start_timestamp,
                        trip_end_timestamp,
                        RANK()
                            OVER (
                                  PARTITION BY pickup_community_area
                                  ORDER BY trip_start_timestamp
                                 ) AS trip_number
                    FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                    WHERE DATE(trip_start_timestamp) = '2013-10-03' 
                    """
trip_number_answer = client.query(trip_number_query).result().to_dataframe()

# (3) BreakTime
break_time_query = """
                   SELECT taxi_id,
                       trip_start_timestamp,
                       trip_end_timestamp,
                       TIMESTAMP_DIFF(
                           trip_start_timestamp, 
                           LAG(trip_end_timestamp, 1) OVER (PARTITION BY taxi_id ORDER BY trip_start_timestamp), 
                           MINUTE) AS prev_break
                   FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                   WHERE DATE(trip_start_timestamp) = '2013-10-03' 
                   """
break_time_answer = client.query(break_time_query).result().to_dataframe()

def run_query(query):
    try:
        results = client.query(query).result().to_dataframe()
    except:
        assert False, "You don't have a valid query yet.  Try again."
    display(results.head())
    return results

# (1)
class TaxiDemand(CodingProblem):
    _var = 'avg_num_trips_query'

    def check(self, query):
        results = run_query(query)
        # check 1: words appear in query
        assert ("over" in query.lower()), ('Your query is missing an **OVER** clause.')
        assert ("3" in query.lower()), ("Your window should include the current date, along with the preceding 3 days and the following 3 days.")
        assert ("avg" in query.lower()), ("Your query should calculate a rolling average.  For this, you need to use the **AVG()** function.")
        # check 2: column names
        lowered_colnames = [c.lower() for c in results.columns]
        assert ('trip_date' in results.columns), ("You didn't select the `trip_date` column. Try again.")
        assert ('avg_num_trips' in results.columns), ("You didn't select the `avg_num_trips` column. Try again.")
        # check 3: length of df
        assert (len(results) == len(avg_num_trips_answer)), ("Your results do not seem to have the correct dates.  You should have one entry "
                                                             "for each date from January 1, 2016, to March 31, 2016.  Note that the provided partial "
                                                             "query already selects the appropriate dates for you (in the `trips_by_day` column).")
        # check 4: check specific value in df
        # get a date to check
        first_date = list(avg_num_trips_answer['trip_date'])[0]
        # get corresponding value  
        correct_number = avg_num_trips_answer.loc[avg_num_trips_answer['trip_date']==first_date]['avg_num_trips'].values[0]
        # want this to equal the corresponding value above
        check_number = results.loc[results['trip_date']==first_date]['avg_num_trips'].values[0]
        assert (int(check_number)==int(correct_number)), ("The results don't look right. Try again.")
    
    _solution = CS(\
"""
avg_num_trips_query = \"""
                      WITH trips_by_day AS
                      (
                      SELECT DATE(trip_start_timestamp) AS trip_date,
                          COUNT(*) as num_trips
                      FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                      WHERE trip_start_timestamp > '2016-01-01' AND trip_start_timestamp < '2016-04-01'
                      GROUP BY trip_date
                      )
                      SELECT trip_date,
                          AVG(num_trips) 
                          OVER (
                               ORDER BY trip_date
                               ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING
                               ) AS avg_num_trips
                      FROM trips_by_day
                      \"""
"""
    )
    _hint = ("Use the **AVG()** function. Write an **OVER** clause with that orders the rows with the `trip_date` column and uses a window that "
             "includes the 3 preceding rows, the current row, and the following 3 rows.")


# (2)
class CommunityArea(CodingProblem):
    _var = 'trip_number_query'
    def check(self, query):
        results = run_query(query)
        # check 1: query contains certain words
        assert ('rank' in query.lower()), ("There are many different numbering functions that enumerate the rows in the input. "
                                           "For this exercise, please use the **RANK()** function.")
        # check 2: correct columns selected
        assert ('pickup_community_area' in set(results.columns)), ("You didn't select the `pickup_community_area` column.")
        assert ('trip_start_timestamp' in set(results.columns)), ("You didn't select the `trip_start_timestamp` column.")
        assert ('trip_end_timestamp' in set(results.columns)), ("You didn't select the `trip_end_timestamp` column.")
        assert ('trip_number' in set(results.columns)), ("You didn't select the `trip_number` column.")
        # check 3: length of df
        assert (len(results)==len(trip_number_answer)), ("Your answer does not have the correct number of rows.")
        # check 4: specific value
        correct_number = len(trip_number_answer.loc[trip_number_answer["trip_number"]==3])
        check_number = len(results.loc[results["trip_number"]==3])
        assert (int(check_number)==int(correct_number)), ("The results don't look right. Try again.")

    _solution = CS( \
"""
trip_number_query = \"""
                    SELECT pickup_community_area,
                        trip_start_timestamp,
                        trip_end_timestamp,
                        RANK()
                            OVER (
                                  PARTITION BY pickup_community_area
                                  ORDER BY trip_start_timestamp
                                 ) AS trip_number
                    FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                    WHERE DATE(trip_start_timestamp) = '2013-10-03' 
                    \"""

trip_number_result = client.query(trip_number_query).result().to_dataframe()
"""
)
    _hint = ("You don't need a **GROUP BY** clause.  Use the **RANK()** function.  Your **OVER** clause should order the rows by the "
             "`trip_start_timestamp` column and break the data into partitions based on `pickup_community_area`.")

# (3)
class BreakTime(CodingProblem):
    _var = 'break_time_query'
    def check(self, query):
        results = run_query(query)
        # check 1: query contains certain words
        assert ('lag' in query.lower()), ("Use the **LAG()** function to pull the value for `trip_end_timestamp` from the previous row.")
        # check 2: correct columns selected
        assert ('taxi_id' in set(results.columns)), ("You didn't select the `taxi_id` column.")
        assert ('trip_start_timestamp' in set(results.columns)), ("You didn't select the `trip_start_timestamp` column.")
        assert ('trip_end_timestamp' in set(results.columns)), ("You didn't select the `trip_end_timestamp` column.")
        assert ('prev_break' in set(results.columns)), ("You didn't select the `prev_break` column.")
        # check 3: check values, length of dataframe
        assert (len(results)==len(break_time_answer)), ("Your answer does not have the correct number of rows.")
        # check 4: specific number
        id_to_check = list(break_time_answer["taxi_id"])[0]
        correct_ans = [int(i) for i in list(break_time_answer.loc[break_time_answer["taxi_id"] == id_to_check]["prev_break"]) if math.isnan(i)==False]
        submitted_ans = [int(i) for i in list(results.loc[results["taxi_id"] == id_to_check]["prev_break"]) if math.isnan(i)==False]
        if len(correct_ans) > 0:
            assert (min(correct_ans)==min(submitted_ans)), ("The results don't look right. Try again.")
            assert (max(correct_ans)==max(submitted_ans)), ("The results don't look right. Try again.")

    _solution = CS( \
"""
break_time_query = \"""
                   SELECT taxi_id,
                       trip_start_timestamp,
                       trip_end_timestamp,
                       TIMESTAMP_DIFF(
                           trip_start_timestamp, 
                           LAG(trip_end_timestamp, 1) OVER (PARTITION BY taxi_id ORDER BY trip_start_timestamp), 
                           MINUTE) as prev_break
                   FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                   WHERE DATE(trip_start_timestamp) = '2013-10-03' 
                   \"""

break_time_result = client.query(break_time_query).result().to_dataframe()
"""
)
    _hint = ("The `TIMESTAMP_DIFF()` function takes three arguments, where the first (`trip_start_timestamp`) and the last (`MINUTE`) "
             "are provided for you.  This function provides the time difference (in minutes) of the timestamps in the first two arguments. "
             "You need only fill in the second argument, which should use the **LAG()** function to pull the timestamp corresponding to "
             "the end of the previous trip (for the same `taxi_id`).")

qvars = bind_exercises(globals(), [
    TaxiDemand,
    CommunityArea,
    BreakTime
    ],
    var_format='q_{n}',
    )

__all__ = list(qvars)
