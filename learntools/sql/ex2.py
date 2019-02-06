import pandas as pd

from learntools.core import *


class WhichCountries(CodingProblem):
    _vars = ['first_query', 'first_results']
    def check(self, query, results):
        assert ("`bigquery-public-data.openaq.global_air_quality`" in query), \
               ('Your query should be pulling data FROM `bigquery-public-data.openaq.global_air_quality`')
        lowered_colnames = [c.lower() for c in results.columns]
        assert ('country' in results.columns), ("You didn't select the country columns. Try again.")
        correct_results_set = {'AE', 'AR', 'AU', 'BH', 'BR', 'CA', 'CL',
                               'CO', 'CW', 'GB', 'IL', 'MX', 'NP', 'PE',
                               'TH', 'TW', 'US', 'UZ', 'ZA'}
        assert (set(results.country) == correct_results_set), ("You have the wrong set of countries. Check your WHERE clause")
        assert (len(results.columns) == 1), ("Nice job. You selected the right countries, but you selected other columns too. "
                                             "See if you can select country without other columns.")
        if results.shape[0] > 19:
            print("You got the right countries. Nice job! Some countries showed up many times in the results. "
                  "To get each country only once you can run `SELECT DISTINCT country ...`. " 
                  "The DISTINCT keyword ensures each column shows up once, which you'll want in some cases.")

    _solution = CS(\
"""
first_query = \"""SELECT country
                  FROM `bigquery-public-data.openaq.global_air_quality`
                  WHERE unit = "ppm"
        \"""

# Or to get each country just once, you could use
first_query = \"""SELECT DISTINCT country
                  FROM `bigquery-public-data.openaq.global_air_quality`
                  WHERE unit = "ppm"
        \"""
"""
    )



class ZeroPollution(CodingProblem):
    _vars = ['zero_pollution_query', 'zero_pollution_results']
    def check(self, query, results):
        assert (type(query) == str), ("You don't have a valid query yet. Try again")
        assert ('select' in query.lower()), ("You don't have a valid query yet. Try again")
        assert ('from' in query.lower()), ("You don't have a valid query yet. Try again")
        assert ('value' in query.lower()), ("You don't have the right WHERE clause yet. Try again")
        assert ('`bigquery-public-data.openaq.global_air_quality`' in query.lower()), \
               ("You should be selecting the data ```FROM `bigquery-public-data.openaq.global_air_quality```s")
        # this is hard to check. The dataset is dynamically updated and new queries are expensive. use min val as something that should't change
        assert(results.timestamp.min() == pd.Timestamp('2015-12-02 01:00:00+0000', tz='UTC')), ("The results don't look right. Try again.")


    _solution = CS( \
"""
zero_pollution_query = \"""SELECT country
                           FROM `bigquery-public-data.openaq.global_air_quality`
                           WHERE value = 0
\"""

zero_pollution_results = open_aq.query_to_pandas_safe(zero_pollution_query)
"""
)

qvars = bind_exercises(globals(), [
    WhichCountries,
    ZeroPollution,
    ],
    tutorial_id=78,
    var_format='q_{n}',
    )

__all__ = list(qvars)
