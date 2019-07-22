import math
import pandas as pd
from google.cloud import bigquery

from learntools.core import *

# Setup 
client = bigquery.Client()

# (1) 
q1_query = """
           SELECT committer.name, COUNT(*) AS num_commits
           FROM `bigquery-public-data.github_repos.sample_commits`
           WHERE committer.date >= '2016-01-01' AND committer.date < '2017-01-01'
           GROUP BY committer.name
           ORDER BY num_commits DESC
           """
q1_df = client.query(q1_query).result().to_dataframe()
q1_answer = int(q1_df.loc[0]['num_commits'])

# (2) QA_One
q_and_a_query = """
                SELECT q.owner_user_id AS owner_user_id,
                    MIN(q.creation_date) AS q_creation_date,
                    MIN(a.creation_date) AS a_creation_date
                FROM `bigquery-public-data.stackoverflow.posts_questions` AS q
                    FULL JOIN `bigquery-public-data.stackoverflow.posts_answers` AS a
                ON q.owner_user_id = a.owner_user_id 
                WHERE q.creation_date >= '2019-01-01' AND q.creation_date < '2019-02-01' 
                    AND a.creation_date >= '2019-01-01' AND a.creation_date < '2019-02-01'
                GROUP BY owner_user_id
                """
q_and_a_answer = client.query(q_and_a_query).result().to_dataframe()

# (3) QA_Two
three_tables_query = """
                     SELECT u.id AS id,
                         MIN(q.creation_date) AS q_creation_date,
                         MIN(a.creation_date) AS a_creation_date
                     FROM `bigquery-public-data.stackoverflow.posts_questions` AS q
                         FULL JOIN `bigquery-public-data.stackoverflow.posts_answers` AS a
                             ON q.owner_user_id = a.owner_user_id 
                         RIGHT JOIN `bigquery-public-data.stackoverflow.users` AS u
                             ON q.owner_user_id = u.id
                     WHERE u.creation_date >= '2019-01-01' and u.creation_date < '2019-02-01'
                     GROUP BY id
                    """
three_tables_answer = client.query(three_tables_query).result().to_dataframe()

# (4) AllUsers
all_users_query = """
                  SELECT q.owner_user_id 
                  FROM `bigquery-public-data.stackoverflow.posts_questions` AS q
                  WHERE EXTRACT(DATE FROM q.creation_date) = '2019-01-01'
                  UNION DISTINCT
                  SELECT a.owner_user_id
                  FROM `bigquery-public-data.stackoverflow.posts_answers` AS a
                  WHERE EXTRACT(DATE FROM a.creation_date) = '2019-01-01'
                  """
all_users_answer = client.query(all_users_query).result().to_dataframe()


# (1)
class MaxCommits(EqualityCheckProblem):
    _var = 'max_commits'
    _expected = q1_answer
    _hint = ("Use `committer.name` and `committer.date` in a query to count the number of rows corresponding "
             "to each committer in 2016. Use a **WHERE** clause, a **GROUP BY** clause, and an **ORDER BY** "
             "clause.")
    _solution = CS(\
"""
max_commits_query = \"""
                    SELECT committer.name, COUNT(*) AS num_commits
                    FROM `bigquery-public-data.github_repos.sample_commits`
                    WHERE committer.date >= '2016-01-01' AND committer.date < '2017-01-01'
                    GROUP BY committer.name
                    ORDER BY num_commits DESC
                    \"""

max_commits = %d
""" % q1_answer
)

# (2)
class QA_One(CodingProblem):
    _vars = ['q_and_a_query', 'q_and_a_result']
    def check(self, query, results):
        # check 1: query contains certain words
        assert ('min' in query.lower()), ("For this exercise, you need only fill in the appropriate **JOIN**.  All other parts of the query should be left as-is.")
        # check 2: correct columns selected
        assert ('owner_user_id' in set(results.columns)), ("You didn't select the `owner_user_id` column.")
        assert ('q_creation_date' in set(results.columns)), ("You didn't select the `q_creation_date` column.")
        assert ('a_creation_date' in set(results.columns)), ("You didn't select the `a_creation_date` column.")
        # check 3: length of df
        assert (len(results)==len(q_and_a_answer)), ("Your answer does not have the correct number of rows.  You should have %d rows, "
                                                         "but you have %d rows." % (len(trip_number_answer), len(results)))

    _solution = CS( \
"""
q_and_a_query = \"""
                SELECT q.owner_user_id AS owner_user_id,
                    MIN(q.creation_date) AS q_creation_date,
                    MIN(a.creation_date) AS a_creation_date
                FROM `bigquery-public-data.stackoverflow.posts_questions` AS q
                    FULL JOIN `bigquery-public-data.stackoverflow.posts_answers` AS a
                ON q.owner_user_id = a.owner_user_id 
                WHERE q.creation_date >= '2019-01-01' AND q.creation_date < '2019-02-01' 
                    AND a.creation_date >= '2019-01-01' AND a.creation_date < '2019-02-01'
                GROUP BY owner_user_id
                \"""

q_and_a_result = client.query(q_and_a_query).result().to_dataframe()
"""
)
    _hint = "Which type of JOIN always returns all rows from both tables?"

# (3)
class QA_Two(CodingProblem):
    _vars = ['three_tables_query', 'three_tables_result']
    def check(self, query, results):
        # check 1: query contains certain words
        assert ('full' in query.lower()), ("Your answer should include a **FULL JOIN**.")
        assert ('users' in query.lower()), ("Don't forget to use the `users` table.")
        assert ('group' in query.lower()), ("You'll need to use a `GROUP BY` clause in your query.")
        # check 2: correct columns selected
        assert ('id' in set(results.columns)), ("You didn't select the `id` column.")
        assert ('q_creation_date' in set(results.columns)), ("You didn't select the `q_creation_date` column.")
        assert ('a_creation_date' in set(results.columns)), ("You didn't select the `a_creation_date` column.")
        # check 3: check values, length of dataframe
        assert (len(results)==len(three_tables_answer)), ("Your answer does not have the correct number of rows. You should have %d rows, "
                                                          "but you have %d rows." % (len(three_tables_answer), len(results)))

    _solution = CS( \
"""
three_tables_query = \"""
                     SELECT u.id AS id,
                         MIN(q.creation_date) AS q_creation_date,
                         MIN(a.creation_date) AS a_creation_date
                     FROM `bigquery-public-data.stackoverflow.posts_questions` AS q
                         FULL JOIN `bigquery-public-data.stackoverflow.posts_answers` AS a
                             ON q.owner_user_id = a.owner_user_id 
                         RIGHT JOIN `bigquery-public-data.stackoverflow.users` AS u
                             ON q.owner_user_id = u.id
                     WHERE u.creation_date >= '2019-01-01' and u.creation_date < '2019-02-01'
                     GROUP BY id
                    \"""

three_tables_result = client.query(three_tables_query).result().to_dataframe()
"""
)
    _hint = \
"""
Here's a partially completed query.  You need only fill in the appropriate JOINs!
```
three_tables_query = \"""
                     SELECT u.id AS id,
                         MIN(q.creation_date) AS q_creation_date,
                         MIN(a.creation_date) AS a_creation_date
                     FROM `bigquery-public-data.stackoverflow.posts_questions` AS q
                         ____ `bigquery-public-data.stackoverflow.posts_answers` AS a
                             ON q.owner_user_id = a.owner_user_id 
                         ____ `bigquery-public-data.stackoverflow.users` AS u
                             ON q.owner_user_id = u.id
                     WHERE u.creation_date >= '2019-01-01' and u.creation_date < '2019-02-01'
                     GROUP BY id
                    \"""
```
"""

# (4)
class AllUsers(CodingProblem):
    _vars = ['all_users_query', 'all_users_result']
    def check(self, query, results):
        # check 1: query contains certain words
        assert ('union' in query.lower()), ("Your query must use a **UNION**.")
        assert ('posts_answers' in query.lower()), ("You must use the `posts_answers` table to answer this question.")
        assert ('posts_questions' in query.lower()), ("You must use the `posts_questions` table to answer this question.")
        # check 2: correct columns selected
        assert ('owner_user_id' in set(results.columns)), ("You didn't select the `owner_user_id` column.")
        assert (len(results.columns)==1), ("Your table has the wrong number of columns.  You should only have one column.")
        # check 3: check values, length of dataframe
        assert (len(results)==len(all_users_answer)), ("Your answer does not have the correct number of rows. You should have %d rows, "
                                                          "but you have %d rows." % (len(all_users_answer), len(results)))

    _solution = CS( \
"""
all_users_query = \"""
                  SELECT q.owner_user_id 
                  FROM `bigquery-public-data.stackoverflow.posts_questions` AS q
                  WHERE EXTRACT(DATE FROM q.creation_date) = '2019-01-01'
                  UNION DISTINCT
                  SELECT a.owner_user_id
                  FROM `bigquery-public-data.stackoverflow.posts_answers` AS a
                  WHERE EXTRACT(DATE FROM a.creation_date) = '2019-01-01'
                  \"""

all_users_answer = client.query(all_users_query).result().to_dataframe()
"""
)
    _hint = ("Begin by writing two separate queries: one to get the user IDs corresponding to questions, and another corresponding "
             "to answers.  Then, take the union of the two columns.")

qvars = bind_exercises(globals(), [
    CorrectQuery,
    QA_One,
    QA_Two,
    AllUsers
    ],
    tutorial_id=-1,
    var_format='q_{n}',
    )

__all__ = list(qvars)
