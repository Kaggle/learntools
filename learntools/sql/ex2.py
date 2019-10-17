import pandas as pd
from google.cloud import bigquery

from learntools.core import *

# Setup (2.42s on Kaggle)
client = bigquery.Client()

# (1) WhichCountries
first_query = """
              SELECT country
              FROM `bigquery-public-data.openaq.global_air_quality`
              WHERE unit = "ppm"
              """
first_query_job = client.query(first_query)
first_results_answer = first_query_job.to_dataframe()

# (2) ZeroPollution
zero_pollution_query = """
                       SELECT *
                       FROM `bigquery-public-data.openaq.global_air_quality`
                       WHERE value = 0
                       """
zero_pollution_query_job = client.query(zero_pollution_query)
zero_pollution_answer = zero_pollution_query_job.to_dataframe()

class WhichCountries(CodingProblem):
    _vars = ['first_query', 'first_results']
    def check(self, query, results):
        # check 1: words appear in query
        assert ("`bigquery-public-data.openaq.global_air_quality`" in query), \
               ('Your query should be pulling data FROM `bigquery-public-data.openaq.global_air_quality`.')
        # check 2: column names
        lowered_colnames = [c.lower() for c in results.columns]
        assert ('country' in results.columns), ("You didn't select the `country` column. Try again.")
        # check 3: values in dataframe
        assert (set(results.country) == set(first_results_answer.country)), ("You have the wrong set of countries. Check your **WHERE** clause.")
        assert (len(results.columns) == 1), ("Nice job. You selected the right countries, but you selected other columns too. "
                                             "See if you can select `country` without other columns.")
        if len(results) == len(first_results_answer):
            print("You got the right countries. Nice job! Some countries showed up many times in the results. "
                  "To get each country only once you can run `SELECT DISTINCT country ...`. " 
                  "The DISTINCT keyword ensures each column shows up once, which you'll want in some cases.")

    _solution = CS(\
"""
first_query = \"""
              SELECT country
              FROM `bigquery-public-data.openaq.global_air_quality`
              WHERE unit = "ppm"
              \"""

# Or to get each country just once, you could use
first_query = \"""
              SELECT DISTINCT country
              FROM `bigquery-public-data.openaq.global_air_quality`
              WHERE unit = "ppm"
              \"""
"""
    )



class ZeroPollution(CodingProblem):
    _vars = ['zero_pollution_query', 'zero_pollution_results']
    def check(self, query, results):
        # check 1: query contains certain words
        assert (type(query) == str), ("You don't have a valid query yet. Try again.")
        assert ('select' in query.lower()), ("You don't have a valid query yet. Try again.")
        assert ('from' in query.lower()), ("You don't have a valid query yet. Try again.")
        assert ('value' in query.lower()), ("You don't have the right **WHERE** clause yet. Try again.")
        assert ('`bigquery-public-data.openaq.global_air_quality`' in query.lower()), \
               ("You should be selecting the data `FROM bigquery-public-data.openaq.global_air_quality`.")
        # check 2: correct columns selected
        assert ('value' in set(results.columns)), ("You didn't select the `value` column.")
        assert (set(results.columns) == set(zero_pollution_answer.columns)), ("Please select **all columns** of the rows where pollution levels were reported to be exactly 0.")
        # check 3: check values, length of dataframe
        assert (all(results["value"]== 0.0)), ("Some rows have a pollution level that is greater than 0.")
        assert(len(results)==len(zero_pollution_answer)), ("The results don't look right. Try again.")

    _solution = CS( \
"""
zero_pollution_query = \"""
                       SELECT *
                       FROM `bigquery-public-data.openaq.global_air_quality`
                       WHERE value = 0
                       \"""

safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
query_job = client.query(zero_pollution_query, job_config=safe_config)

zero_pollution_results = query_job.to_dataframe()
"""
)

qvars = bind_exercises(globals(), [
    WhichCountries,
    ZeroPollution,
    ],
    var_format='q_{n}',
    )

__all__ = list(qvars)
