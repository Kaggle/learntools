from google.cloud import bigquery
import numpy as np
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

# (1)
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

# (2)
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

# (3)
class SelectRightQuestions(CodingProblem):
    _vars = ['questions_query', 'questions_results']
    def check(self, query, results):
        # check 1: words appear in query
        lower_query = query.lower()
        results.columns = [c.lower() for c in results.columns]
        assert ('like \'%bigquery%\'' in lower_query), ('Your **WHERE** clause is not filtering on the "bigquery" tag correctly.')
        assert ('id' in results.columns), ('Should have `id` in the columns. Your column names are {}.'.format(results.columns))
        # check 2: column names
        assert (results.shape[1] == 3), ('You should have 3 columns. But you have {}. Your list of columns is {}.'.format(len(results.columns), results.columns))
        # check 3: check dataframe length
        assert(len(results)==len(questions_answer)), ("Your results do not have the correct number of rows.  You may not have the right **WHERE** clause.")
        # check 4: IDs
        correct_ids = set(questions_answer['id'])
        user_ids = set(results['id'])
        assert (correct_ids == user_ids), ('You do not have the correct values in the `id` column.')
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
safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
questions_query_job = client.query(questions_query, job_config=safe_config)

# API request - run the query, and return a pandas DataFrame
questions_results = questions_query_job.to_dataframe()
"""
)

# (4)
class FirstJoin(CodingProblem):
    _vars = ['answers_query', 'answers_results']
    def check(self, query, results):
        # check 1: words appear in query
        lower_query = query.lower()
        assert ('like \'%bigquery%\'' in lower_query), ('Your **WHERE** clause is not filtering on the "bigquery" tag correctly.')
        assert ('join' in lower_query), ('Your query does not include a **JOIN** statement.')
        # check 2: column names
        results.columns = [c.lower() for c in results.columns]
        assert ('id' in results.columns), ('You should have a column named `id`. Your columns are {}.'.format(results.columns))
        assert ('body' in results.columns), ('You should have a column named `body`. Your columns are {}.'.format(results.columns))
        assert ('owner_user_id' in results.columns), ('You should have a column named `owner_user_id`. Your columns are {}.'.format(results.columns))
        # check 3: pulled correct IDs
        correct_ids = set([int(i) for i in answers_answer.id.values if not np.isnan(i)])
        submitted_ids = set([int(i) for i in results.id.values if not np.isnan(i)])
        assert (correct_ids == submitted_ids), ('You seem to have the wrong values in the `id` column.')
        # check 4: check one value from other two columns
        first_id = list(answers_answer["id"].values)[0]
        correct_owner_user_id = int(answers_answer[answers_answer["id"] == first_id]["owner_user_id"])
        submitted_owner_user_id = int(results[results["id"] == first_id]["owner_user_id"])
        assert (correct_owner_user_id == submitted_owner_user_id), ('The values in the `owner_user_id` column appear to be incorrect.')

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
# your quota, with the limit set to 27 GB)
safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=27*10**10)
answers_query_job = client.query(answers_query, job_config=safe_config)

# API request - run the query, and return a pandas DataFrame
answers_results = answers_query_job.to_dataframe()
"""
)

# (5)
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
safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
bigquery_experts_query_job = client.query(bigquery_experts_query, job_config=safe_config)

# API request - run the query, and return a pandas DataFrame
bigquery_experts_results = bigquery_experts_query_job.to_dataframe()
"""
)
    def check(self, query, results):
        # check 1: words appear in query
        lower_query = query.lower()
        assert ('group by' in lower_query), ('Your query should have a **GROUP BY** clause.')
        assert ('count' in lower_query), ('Your query should have a **COUNT** in the **SELECT** statement.')
        assert ('%bigquery' in lower_query), ('Your **WHERE** clause is not filtering on the "bigquery" tag correctly.')
        # check 2: column names
        results.columns = [c.lower() for c in results.columns]
        assert ('user_id' in results.columns), ('You do not have a `user_id` column in your results.')
        assert ('number_of_answers' in results.columns), ('You do not have a `number_of_answers` column in your results.')
        # check 3: correct user IDs
        correct_ids = set([int(i) for i in bigquery_experts_answer.user_id.values if not np.isnan(i)])
        submitted_ids = set([int(i) for i in results.user_id.values if not np.isnan(i)])
        assert (correct_ids == submitted_ids), ('You seem to have the wrong values in the `user_id` column.')
        # check 4: check one value from other column
        first_id = list(bigquery_experts_answer["user_id"])[0]
        correct_num = int(bigquery_experts_answer[bigquery_experts_answer["user_id"] == first_id]["number_of_answers"])
        submitted_num = int(results[results["user_id"] == first_id]["number_of_answers"])
        assert (correct_num == submitted_num), ('The values in the `number_of_answers` column appear to be incorrect.')

# (6)
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
               WHERE q.tags like '%{topic}%'
               GROUP BY a.owner_user_id
               \"""
               
    # Set up the query (a real service would have good error handling for 
    # queries that scan too much data)
    safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)      
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
    var_format='q_{n}',
    )

__all__ = list(qvars)
