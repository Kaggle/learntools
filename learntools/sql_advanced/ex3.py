import math
import pandas as pd
from google.cloud import bigquery

from learntools.core import *

# Setup 
client = bigquery.Client()

# (1) 
q1_query = """
           SELECT committer.name AS committer_name, COUNT(*) AS num_commits
           FROM `bigquery-public-data.github_repos.sample_commits`
           WHERE committer.date >= '2016-01-01' AND committer.date < '2017-01-01'
           GROUP BY committer_name
           ORDER BY num_commits DESC
           """
q1_answer = client.query(q1_query).result().to_dataframe()


# (3) QA_One
q3_query = """
           SELECT l.name as language_name, COUNT(*) as num_repos
           FROM `bigquery-public-data.github_repos.languages`,
               UNNEST(language) AS l
           GROUP BY language_name
           ORDER BY num_repos DESC
           """
q3_answer = client.query(q3_query).result().to_dataframe()

# (4) AllLangs
q4_query = """
           SELECT l.name, l.bytes
           FROM `bigquery-public-data.github_repos.languages`,
               UNNEST(language) as l
           WHERE repo_name = 'polyrabbit/polyglot'
           ORDER BY l.bytes DESC
           """
q4_answer = client.query(q4_query).result().to_dataframe()


def run_query(query):
    try:
        results = client.query(query).result().to_dataframe()
    except:
        assert False, "You don't have a valid query yet.  Try again."
    display(results.head())
    return results

# (1)
class MaxCommits(CodingProblem):
    _var = 'max_commits_query'
    def check(self, query):
        results = run_query(query)
        # check 1: query contains certain words
        assert ('committer.name' in query.lower()), ("Your query should use the \"name\" field in the \"committer\" column.")
        assert ('committer.date' in query.lower()), ("Your query should use the \"date\" field in the \"committer\" column.")
        assert ('sample_commits' in query.lower()), ("Your query should use the `sample_commits` table.")
        assert ('order by' in query.lower()), ("Sort the table, so that people with more commits appear first.")
        assert ('desc' in query.lower()), ("Sort the table, so that people with more commits appear first.")
        # check 2: correct columns selected
        assert ('committer_name' in set(results.columns)), ("You didn't select the `committer_name` column.")
        assert ('num_commits' in set(results.columns)), ("You didn't select the `num_commits` column.")
        # check 3: length of df
        assert (len(results)==len(q1_answer)), ("Your answer does not have the correct number of rows.  You should have %d rows, "
                                                         "but you have %d rows." % (len(q1_answer), len(results)))
        # check 4: specific value
        first_name = list(q1_answer['committer_name'])[0]
        correct_number = q1_answer.loc[q1_answer['committer_name']==first_name]['num_commits'].values[0]
        check_number = results.loc[results['committer_name']==first_name]['num_commits'].values[0]
        assert (int(correct_number)==int(check_number)), ("The results don't look right. Try again.")

    _hint = ("Use `committer.name` and `committer.date` in a query to count the number of rows corresponding "
             "to each committer in 2016. Use a **WHERE** clause, a **GROUP BY** clause, and an **ORDER BY** "
             "clause.")
    _solution = CS(\
"""
max_commits_query = \"""
                    SELECT committer.name AS committer_name, COUNT(*) AS num_commits
                    FROM `bigquery-public-data.github_repos.sample_commits`
                    WHERE committer.date >= '2016-01-01' AND committer.date < '2017-01-01'
                    GROUP BY committer_name
                    ORDER BY num_commits DESC
                    \"""
""" 
)
    
# (2)
class LookLang(EqualityCheckProblem):
    _var = 'num_rows'
    _expected = 6
    _hint = \
"""Remember that the **UNNEST()** function essentially flattens the repeated data (which is then appended to the right side of the table) so that we have one element on each row."""

    _solution = CS(
"""
num_rows = 6
"""
)
    
# (3)
class PopLang(CodingProblem):
    _var = 'pop_lang_query'
    def check(self, query):
        results = run_query(query)
        # check 1: query contains certain words
        assert ('languages' in query.lower()), ("You need to query the `languages` table.")
        assert ('unnest' in query.lower()), ("You need to use the **UNNEST()** function.")
        assert ('order by' in query.lower()), ("Order the rows in the table so that languages that can be found in more repos appear first.")
        assert ('desc' in query.lower()), ("Order the rows in the table so that languages that can be found in more repos appear first.")
        # check 2: correct columns selected
        assert ('language_name' in set(results.columns)), ("You didn't select the `language_name` column.")
        assert ('num_repos' in set(results.columns)), ("You didn't select the `num_repos` column.")
        # check 3: length of df
        assert (len(results)==len(q3_answer)), ("Your answer does not have the correct number of rows.  You should have %d rows, "
                                                         "but you have %d rows." % (len(q3_answer), len(results)))
        # check 4: specific value
        first_lang = list(q3_answer['language_name'])[0]
        correct_number = q3_answer.loc[q3_answer['language_name']==first_lang]['num_repos'].values[0]
        check_number = results.loc[results['language_name']==first_lang]['num_repos'].values[0]
        assert (int(correct_number)==int(check_number)), ("The results don't look right. Try again.")

    _solution = CS( \
"""
pop_lang_query = \"""
                 SELECT l.name as language_name, COUNT(*) as num_repos
                 FROM `bigquery-public-data.github_repos.languages`,
                     UNNEST(language) AS l
                 GROUP BY language_name
                 ORDER BY num_repos DESC
                 \"""
"""
)
    _hint = "The \"language\" column contains repeated data!"

# (4)
class AllLangs(CodingProblem):
    _var = 'all_langs_query'
    def check(self, query):
        results = run_query(query)
        # check 1: query contains certain words
        assert ('languages' in query.lower()), ("You need to query the `languages` table.")
        assert ('unnest' in query.lower()), ("You need to use the **UNNEST()** function.")
        assert ('polyglot' in query.lower()), ("Restrict your attention to the `'polyrabbit/polyglot'` repository.")
        assert ('where' in query.lower()), ("Restrict your attention to the `'polyrabbit/polyglot'` repository.")
        assert ('order' in query.lower()), ("Sort the table by the `bytes` column so that programming languages that take up more space in the repo appear first.")
        assert ('desc' in query.lower()), ("Sort the table by the `bytes` column so that programming languages that take up more space in the repo appear first.")
        # check 2: correct columns selected
        assert ('name' in set(results.columns)), ("You didn't select the `name` column.")
        assert ('bytes' in set(results.columns)), ("You didn't select the `bytes` column.")
        # check 3: check values, length of dataframe
        assert (len(results)==len(q4_answer)), ("Your answer does not have the correct number of rows. You should have %d rows, "
                                                          "but you have %d rows." % (len(q4_answer), len(results)))
        # check 4: specific value
        first_lang = list(q4_answer['name'])[0]
        correct_number = q4_answer.loc[q4_answer['name']==first_lang]['bytes'].values[0]
        check_number = results.loc[results['name']==first_lang]['bytes'].values[0]
        assert (int(correct_number)==int(check_number)), ("The results don't look right. Try again.")

    _solution = CS( \
"""
all_langs_query = \"""
                  SELECT l.name, l.bytes
                  FROM `bigquery-public-data.github_repos.languages`,
                      UNNEST(language) as l
                  WHERE repo_name = 'polyrabbit/polyglot'
                  ORDER BY l.bytes DESC
                  \"""
"""
)
    _hint = \
"""
The \"language\" column contains repeated data!  You'll need to use a **WHERE** clause and an **ORDER BY** clause.
"""

qvars = bind_exercises(globals(), [
    MaxCommits,
    LookLang,
    PopLang,
    AllLangs
    ],
    var_format='q_{n}',
    )

__all__ = list(qvars)
