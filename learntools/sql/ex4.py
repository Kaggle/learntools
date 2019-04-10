from google.cloud import bigquery

from learntools.core import *

# Setup (2.4s on Kaggle)
client = bigquery.Client()

# (1) EducationSpending
country_spend_pct_query = """
                          SELECT country_name, AVG(value) AS avg_ed_spending_pct
                          FROM `bigquery-public-data.world_bank_intl_education.international_education`
                          WHERE indicator_code = 'SE.XPD.TOTL.GD.ZS' and year >= 2010 and year <= 2017
                          GROUP BY country_name
                          ORDER BY avg_ed_spending_pct DESC
                          """
country_spend_pct_query_job = client.query(country_spend_pct_query)
country_spending_answer = country_spend_pct_query_job.to_dataframe()

# (2) FindInterestingCodes
code_count_query = """
                   SELECT indicator_code, indicator_name, COUNT(1) AS num_rows
                   FROM `bigquery-public-data.world_bank_intl_education.international_education`
                   WHERE year = 2016
                   GROUP BY indicator_name, indicator_code
                   HAVING COUNT(1) >= 175
                   ORDER by COUNT(1) DESC
                   """
code_count_query_job = client.query(code_count_query)
interesting_codes_answer = code_count_query_job.to_dataframe()


class EducationSpending(CodingProblem):
    _vars = ['country_spend_pct_query', 'country_spending_results']
    def check(self, query, results):
        lower_query = query.lower()
        assert ('des' in lower_query), ("You should use `DESC` in your **ORDER BY** clause.")
        assert (('2017' in lower_query) or ('2018' in lower_query)), ('You should have `year <= 2017` in your query.')
        assert ('avg_ed_spending_pct' in [c.lower() for c in results.columns]), ('Your column names were {}. They should include `avg_ed_spending_pct`.'.format(results.columns))
        assert (results.equals(country_spending_answer)), ("The results don't look right. Try again.")

    _hint = "The part before `FROM` should be `SELECT country_name, AVG(value) avg_ed_spending_pct`."
    _solution = CS(\
"""
country_spend_pct_query = \"""
                          SELECT country_name, AVG(value) AS avg_ed_spending_pct
                          FROM `bigquery-public-data.world_bank_intl_education.international_education`
                          WHERE indicator_code = 'SE.XPD.TOTL.GD.ZS' and year >= 2010 and year <= 2017
                          GROUP BY country_name
                          ORDER BY avg_ed_spending_pct DESC
                          \"""

"""
)

class FindInterestingCodes(CodingProblem):
    _vars = ['code_count_query', 'code_count_results']
    def check(self, query, results):
        results.columns = [c.lower() for c in results.columns]
        lower_query = query.lower()
        assert ("having" in lower_query), ('You are missing your **HAVING** clause.')
        assert ("order" in lower_query), ('You are missing your **ORDER BY** clause.')
        assert (results.equals(interesting_codes_answer)), ("The results don't look right. Try again.")
    _hint = "The part before `FROM` is `SELECT indicator_code, indicator_name, COUNT(1) AS num_rows`."
    _solution = CS(\
"""
code_count_query = \"""
                   SELECT indicator_code, indicator_name, COUNT(1) AS num_rows
                   FROM `bigquery-public-data.world_bank_intl_education.international_education`
                   WHERE year = 2016
                   GROUP BY indicator_name, indicator_code
                   HAVING COUNT(1) >= 175
                   ORDER BY COUNT(1) DESC
                   \"""
"""
)


qvars = bind_exercises(globals(), [
    EducationSpending,
    FindInterestingCodes
    ],
    tutorial_id=80,
    var_format='q_{n}',
    )

__all__ = list(qvars)
