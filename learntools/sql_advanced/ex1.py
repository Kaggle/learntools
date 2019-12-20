import math
import pandas as pd
from google.cloud import bigquery

from learntools.core import *

# Setup 
client = bigquery.Client()

# (1) CorrectQuery
correct_query = """
                SELECT q.id AS q_id,
                    MIN(TIMESTAMP_DIFF(a.creation_date, q.creation_date, SECOND)) as time_to_answer
                FROM `bigquery-public-data.stackoverflow.posts_questions` AS q
                    LEFT JOIN `bigquery-public-data.stackoverflow.posts_answers` AS a
                ON q.id = a.parent_id
                WHERE q.creation_date >= '2018-01-01' and q.creation_date < '2018-02-01'
                GROUP BY q_id
                ORDER BY time_to_answer
                """
correct_answer = client.query(correct_query).result().to_dataframe()

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

def run_query(query):
    try:
        results = client.query(query).result().to_dataframe()
    except:
        assert False, "You don't have a valid query yet.  Try again."
    display(results.head())
    return results

# (1)
class CorrectQuery(CodingProblem):
    _var = 'correct_query'
    def check(self, query):
        results = run_query(query)
        # check 1: length of df
        assert (len(results) == len(correct_answer)), ("You don't have the correct number of rows in your submission.  You should have "
                                                       "%d rows, but you have %d rows." % (len(correct_answer), len(results)))
        # check 2: calculated values
        # correct result
        correct_list = [i for i in list(correct_answer["time_to_answer"]) if not math.isnan(i)]
        correct_number = int(sum(correct_list)/len(correct_list))
        # submitted value
        submitted_list = [i for i in list(results["time_to_answer"]) if not math.isnan(i)]
        submitted_number = int(sum(submitted_list)/len(submitted_list))
        assert (int(submitted_number)==int(correct_number)), ("The results don't look right. Please make sure that the part of the query "
                                                              "that calculates the values in the `time_to_answer` column is unmodified.")
    
    _solution = CS(\
"""
correct_query = \"""
                SELECT q.id AS q_id,
                    MIN(TIMESTAMP_DIFF(a.creation_date, q.creation_date, SECOND)) as time_to_answer
                FROM `bigquery-public-data.stackoverflow.posts_questions` AS q
                    LEFT JOIN `bigquery-public-data.stackoverflow.posts_answers` AS a
                ON q.id = a.parent_id
                WHERE q.creation_date >= '2018-01-01' and q.creation_date < '2018-02-01'
                GROUP BY q_id
                ORDER BY time_to_answer
                \"""
"""
    )
    _hint = ("Is the `posts_questions` table the **LEFT** or **RIGHT** table?  You want to keep all of the rows from this table, regardless of "
             "whether or not there is a match in the `posts_answers` table.")


# (2)
class QA_One(CodingProblem):
    _var = 'q_and_a_query'
    def check(self, query):
        results = run_query(query)
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
"""
)
    _hint = "Which type of JOIN always returns all rows from both tables?"

# (3)
class QA_Two(CodingProblem):
    _var = 'three_tables_query'
    def check(self, query):
        results = run_query(query)
        # check 1: query contains certain words
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
                     FROM `bigquery-public-data.stackoverflow.users` AS u
                         LEFT JOIN `bigquery-public-data.stackoverflow.posts_answers` AS a
                             ON u.id = a.owner_user_id
                         LEFT JOIN `bigquery-public-data.stackoverflow.posts_questions` AS q
                             ON q.owner_user_id = u.id
                     WHERE u.creation_date >= '2019-01-01' and u.creation_date < '2019-02-01'
                     GROUP BY id
                    \"""
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
                     FROM `bigquery-public-data.stackoverflow.users` AS u
                         ____ `bigquery-public-data.stackoverflow.posts_answers` AS a
                             ON u.id = a.owner_user_id
                         ____ `bigquery-public-data.stackoverflow.posts_questions` AS q
                             ON q.owner_user_id = u.id
                     WHERE u.creation_date >= '2019-01-01' and u.creation_date < '2019-02-01'
                     GROUP BY id
                    \"""
```
"""

# (4)
class AllUsers(CodingProblem):
    _var = 'all_users_query'
    def check(self, query):
        results = run_query(query)
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
    var_format='q_{n}',
    )

__all__ = list(qvars)
