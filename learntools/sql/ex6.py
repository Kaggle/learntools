from google.cloud import bigquery

from learntools.core import *

# Setup (7.42s on Kaggle)
client = bigquery.Client()

# (1) ListSOTables
dataset_ref = client.dataset("stackoverflow", project="bigquery-public-data")
dataset = client.get_dataset(dataset_ref)
tables = list(client.list_tables(dataset))
list_of_tables_answer = [table.table_id for table in tables] 

# (3) SelectRightQuestions
questions_query = """
                  SELECT id, title, owner_user_id
                  FROM `bigquery-public-data.stackoverflow.posts_questions`
                  WHERE tags like '%bigquery%'
                  """
questions_query_job = client.query(questions_query)
questions_answer = questions_query_job.to_dataframe()

# (4) FirstJoin
answers_query = """
                SELECT a.id, a.body, a.owner_user_id
                FROM `bigquery-public-data.stackoverflow.posts_questions` AS q 
                INNER JOIN `bigquery-public-data.stackoverflow.posts_answers` AS a
                    ON q.id = a.parent_id
                WHERE q.tags LIKE '%bigquery%'
                """
answers_query_job = client.query(answers_query)
answers_answer = answers_query_job.to_dataframe()

# (5) BigQueryExperts
bigquery_experts_query = """
                         SELECT a.owner_user_id AS user_id, COUNT(1) AS number_of_answers
                         FROM `bigquery-public-data.stackoverflow.posts_questions` AS q
                         INNER JOIN `bigquery-public-data.stackoverflow.posts_answers` AS a
                             ON q.id = a.parent_Id
                         WHERE q.tags LIKE '%bigquery%'
                         GROUP BY a.owner_user_id
                         """
bigquery_experts_query_job = client.query(bigquery_experts_query)
bigquery_experts_answer = bigquery_experts_query_job.to_dataframe()


class ListSOTables(EqualityCheckProblem):
    _var = 'list_of_tables'
    _expected = list_of_tables_answer
    _solution = CS(
"""
# Get a list of available tables 
tables = list(client.list_tables(dataset))
list_of_tables = [table.table_id for table in tables] 
"""
)

class HowToFindExperts(ThoughtExperiment):
    _solution = \
"""
`posts_questions` has a column called `tags` which lists the topics/technologies each question is about.

`posts_answers` has a column called `parent_id` which identifies the ID of the question each answer is responding to.
`posts_answers` also has an `owner_user_id` column which specifies the ID of the user who answered the question.

You can join these two tables to:
- determine the `tags` for each answer, and then
- select the `owner_user_id` of the answers on the desired tag.

This is exactly what you will do over the next few questions.
"""

class SelectRightQuestions(CodingProblem):
    _vars = ['questions_query', 'questions_results']
    def check(self, query, results):
        lower_query = query.lower()
        results.columns = [c.lower() for c in results.columns]
        assert ('like \'%bigquery%\'' in lower_query), ('Your **WHERE** clause is not filtering on the "bigquery" tag correctly.')
        assert ('id' in results.columns), ('Should have `id` in the columns. Your column names are {}.'.format(results.columns))
        assert (results.shape[1] == 3), ('You should have 3 columns. But you have {}. Your list of columns is {}.'.format(len(results.columns), results.columns))
        if not results.equals(questions_answer):
            assert (34798244 in results.id.values), ('You seem to be missing some relevant values from the `id` column.')
            assert (results.shape[0] < 20000), ('Your results have too many rows in the response. You may not have the right **WHERE** clause.')
        assert (results.equals(questions_answer)), ("The results don't look right. Try again.")
    _hint = 'Your **WHERE** clause should be `WHERE tags LIKE \'%bigquery%\'`.'
    _solution = CS(
"""
questions_query = \"""
                  SELECT id, title, owner_user_id
                  FROM `bigquery-public-data.stackoverflow.posts_questions`
                  WHERE tags LIKE '%bigquery%'
                  \"""

# Set up the query (cancel the query if it would use too much of 
# your quota, with the limit set to 1 GB)
safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=1e9)
questions_query_job = client.query(questions_query, job_config=safe_config)

# API request - run the query, and return a pandas DataFrame
questions_results = questions_query_job.to_dataframe()
"""
)

class FirstJoin(CodingProblem):
    _vars = ['answers_query', 'answers_results']
    def check(self, query, results):
        lower_query = query.lower()
        results.columns = [c.lower() for c in results.columns]
        assert ('like \'%bigquery%\'' in lower_query), ('Your **WHERE** clause is not filtering on the "bigquery" tag correctly.')
        assert ('join' in lower_query), ('Your query does not include a **JOIN** statement.')
        assert ('id' in results.columns), ('You should have a column named `id`. Your columns are {}.'.format(results.columns))
        if not results.equals(answers_answer):
            assert (21592157 in results.id.values), ('You seem to be missing some relevant values from the `id` column.')
            assert (results.shape[0] < 20000), ('You have {} rows in your results. It should be closer to 10500. You may have the wrong **WHERE** clause.')
        assert (results.equals(answers_answer)), ("The results don't look right. Try again.")
    _hint = \
"""
Do an **INNER JOIN** between `bigquery-public-data.stackoverflow.posts_questions` and `bigquery-public-data.stackoverflow.posts_answers`.

Give `post_questions` an alias of `q`, and use `a` as an alias for `posts_answers`. The **ON** part of your join is `q.id = a.parent_id`.
"""
    _solution = CS(\
"""
answers_query = \"""
                SELECT a.id, a.body, a.owner_user_id
                FROM `bigquery-public-data.stackoverflow.posts_questions` AS q 
                INNER JOIN `bigquery-public-data.stackoverflow.posts_answers` AS a
                    ON q.id = a.parent_id
                WHERE q.tags LIKE '%bigquery%'
                \"""
                
# Set up the query (cancel the query if it would use too much of 
# your quota, with the limit set to 1 GB)
safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=1e9)
answers_query_job = client.query(answers_query, job_config=safe_config)

# API request - run the query, and return a pandas DataFrame
answers_results = answers_query_job.to_dataframe()
"""
)

class BigQueryExperts(CodingProblem):
    _vars = ['bigquery_experts_query', 'bigquery_experts_results']
    _hint = "Start with `SELECT a.owner_user_id AS user_id, COUNT(1) AS number_of_answers`"
    _solution = CS(
"""
bigquery_experts_query = \"""
                         SELECT a.owner_user_id AS user_id, COUNT(1) AS number_of_answers
                         FROM `bigquery-public-data.stackoverflow.posts_questions` AS q
                         INNER JOIN `bigquery-public-data.stackoverflow.posts_answers` AS a
                             ON q.id = a.parent_Id
                         WHERE q.tags LIKE '%bigquery%'
                         GROUP BY a.owner_user_id
                         \"""

# Set up the query (cancel the query if it would use too much of 
# your quota, with the limit set to 1 GB)
safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=1e9)
bigquery_experts_query_job = client.query(bigquery_experts_query, job_config=safe_config)

# API request - run the query, and return a pandas DataFrame
bigquery_experts_results = bigquery_experts_query_job.to_dataframe()
"""
)
    def check(self, query, results):
        lower_query = query.lower()
        results.columns = [c.lower() for c in results.columns]
        assert ('group by' in lower_query), ('Your query should have a **GROUP BY** clause.')
        assert ('count' in lower_query), ('Your query should have a **COUNT** in the **SELECT** statement.')
        assert ('%bigquery' in lower_query), ('Your **WHERE** clause is not filtering on the "bigquery" tag correctly.')
        assert ('user_id' in results.columns), ('You do not have a `user_id` column in your results.')
        assert ('number_of_answers' in results.columns), ('You do not have a `number_of_answers` column in your results.')
        if not results.equals(bigquery_experts_answer):
            # Correct answer has 2151 rows at time this code was written
            rows_in_result = results.shape[0]
            assert (rows_in_result < 10000), ('Your result has too many rows ({} rows). Something is wrong'.format(rows_in_result))
            assert (rows_in_result > 2000), ('Your result has too few rows ({} rows). Something is wrong'.format(rows_in_result))
            assert (212435 in results.user_id.values), ('Your results did not return the right set of user id\'s.')
        assert (results.equals(bigquery_experts_answer)), ("The results don't look right. Try again.")


class GeneralizeExpertFinder(ThoughtExperiment):
    _solution = CS(
"""
def expert_finder(topic, client):
    '''
    Returns a DataFrame with the user IDs who have written Stack Overflow answers on a topic.

    Inputs:
        topic: A string with the topic of interest
        client: A Client object that specifies the connection to the Stack Overflow dataset

    Outputs:
        results: A DataFrame with columns for user_id and number_of_answers. Follows similar logic to bigquery_experts_results shown above.
    '''
    my_query = \"""
               SELECT a.owner_user_id AS user_id, COUNT(1) AS number_of_answers
               FROM `bigquery-public-data.stackoverflow.posts_questions` AS q
               INNER JOIN `bigquery-public-data.stackoverflow.posts_answers` AS a
                   ON q.id = a.parent_Id
               WHERE q.tags like '%' + tag + '%'
               GROUP BY a.owner_user_id
               \"""
               
    # Set up the query (a real service would have good error handling for 
    # queries that scan too much data)
    safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=1e9)      
    my_query_job = client.query(my_query, job_config=safe_config)
    
    # API request - run the query, and return a pandas DataFrame
    results = my_query_job.to_dataframe()

    return results
"""
)


qvars = bind_exercises(globals(), [
    ListSOTables,
    HowToFindExperts,
    SelectRightQuestions,
    FirstJoin,
    BigQueryExperts,
    GeneralizeExpertFinder
    ],
    tutorial_id=82,
    var_format='q_{n}',
    )

__all__ = list(qvars)
