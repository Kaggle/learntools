from learntools.core import *


class ListSOTables(EqualityCheckProblem):
    _var = 'list_of_tables'
    _expected = \
['badges',
 'comments',
 'post_history',
 'post_links',
 'posts_answers',
 'posts_moderator_nomination',
 'posts_orphaned_tag_wiki',
 'posts_privilege_wiki',
 'posts_questions',
 'posts_tag_wiki',
 'posts_tag_wiki_excerpt',
 'posts_wiki_placeholder',
 'stackoverflow_posts',
 'tags',
 'users',
 'votes']
    _solution = CS('list_of_tables = stack_overflow.list_tables()')

class HowToFindExperts(ThoughtExperiment):
    _solution = \
"""
`posts_questions` has a column called `tags` which lists the topics/technologies each question is about.

`posts_answers` has a column called `parent_id` which identifies the id of the question each answer is responding to.
`posts_answers` also has an `owner_user_id` column which specifies the user_id that wrote each answer.

You can join these two tables to determine the `tags` for each answer.

Then select the `owner_user_id` of the answers on the desired tag.

This is exactly what you will do over the next few questions.
"""

class SelectRightQuestions(CodingProblem):
    _vars = ['questions_query', 'questions_results']
    def check(self, query, results):
        lower_query = query.lower()
        results.columns = [c.lower() for c in results.columns]
        assert ('like \'%bigquery%\'' in lower_query), ('Your `WHERE` clause is not filtering on the bigquery tag correctly')
        assert ('id' in results.columns), ('Should have `id` in the response columns. Your column names are {}'.format(results.columns))
        assert (34798244 in results.id.values), ('You seem to be missing some relevant values from the id columns')
        assert (results.shape[1] == 3), ('You should have 3 columns. But you have {}. Your list of columns is'.format(len(results.columns), results.columns))
        assert (results.shape[0] < 20000), ('Your results have too many rows in the response. You may not have the right WHERE clause')
    _hint = 'Your WHERE clause should be `WHERE tags like \'%bigquery%\'`'
    _solution = CS(
"""
questions_query = \
\"""
SELECT id, title, owner_user_id
FROM `bigquery-public-data.stackoverflow.posts_questions`
WHERE tags like '%bigquery%'
\"""

questions_results=stack_overflow.query_to_pandas_safe(my_query, max_gb_scanned=2)
"""
)

class FirstJoin(CodingProblem):
    _vars = ['answers_query', 'answers_results']
    def check(self, query, results):
        lower_query = query.lower()
        results.columns = [c.lower() for c in results.columns]
        assert ('like \'%bigquery%\'' in lower_query), ('Your `WHERE` clause is not filtering on the bigquery tag correctly')
        assert ('join' in lower_query), ('Your query does not include a join statement')
        assert ('id' in results.columns), ('You should have a column named `answer_id`. Your columns are {}'.format(results.columns))
        assert (21592157 in results.id.values), ('You seem to be missing some relevant values from the `answer_id` columns')
        assert (results.shape[0] < 20000), ('You have {} rows in your results. It should be closer to 10500. You may the wrong WHERE clause')


    _hint = """Do an inner JOIN between `bigquery-public-data.stackoverflow.posts_questions` and  `bigquery-public-data.stackoverflow.posts_answers`.

    You will want to give both of them aliases. Call `post_questions` q and call `posts_answers` a. The `ON` part of your join is `q.id = a.parent_id`
    """
    _solution = CS(\
"""
answers_query = \"""
SELECT a.id, a.body, a.owner_user_id
FROM `bigquery-public-data.stackoverflow.posts_questions` q INNER JOIN `bigquery-public-data.stackoverflow.posts_answers` a
     ON q.id = a.parent_id
     WHERE q.tags like '%bigquery%'
\"""
"""
)

class BigQueryExperts(CodingProblem):
    _vars = ['bigquery_experts_query', 'bigquery_experts_results']
    _hint = "Start with `SELECT a.owner_user_id AS user_id, COUNT(1) number_of_answers`"
    _solution = CS(
"""
bigquery_experts_query = \"""SELECT a.owner_user_id AS user_id, COUNT(1) number_of_answers
                  FROM `bigquery-public-data.stackoverflow.posts_questions` q
                        INNER JOIN `bigquery-public-data.stackoverflow.posts_answers` a
                        ON q.id = a.parent_Id
                  WHERE q.tags like '%bigquery%'
                  GROUP BY a.owner_user_id\"""

bigquery_experts_results = stack_overflow.query_to_pandas_safe(bigquery_experts_query, max_gb_scanned=2)
"""
    )
    def check(self, query, results):
        lower_query = query.lower()
        results.columns = [c.lower() for c in results.columns]
        assert ('group by' in lower_query), ('Your query should have a GROUP BY clause')
        assert ('count' in lower_query), ('Your query should have a COUNT in the SELECT statement')
        assert ('%bigquery' in lower_query), ('Your query should have `tags like %bigquery%` in the WHERE clause')

        assert ('user_id' in results.columns), ('You do not have a `user_id` column in your results')
        assert ('number_of_answers' in results.columns), ('You do not have a `number_of_answers` column in your results')
        # Correct answer has 2151 rows at time this code was written
        rows_in_result = results.shape[0]
        assert (rows_in_result < 10000), ('Your result has too many rows ({} rows). Something is wrong'.format(rows_in_result))
        assert (rows_in_result > 2000), ('Your result has too few rows ({} rows). Something is wrong'.format(rows_in_result))
        assert (212435 in results.user_id.values), ('Your results did not return the right set of user id\'s.')


class GeneralizeExpertFinder(ThoughtExperiment):
    _solution = CS(
"""
def expert_finder(topic, stack_overflow_helper):
    '''
    Returns a DataFrame with the user_id's who have written stackoverflow answers on topic.

    Inputs:
        topic: A string with the topic we are interested
        stack_overflow_helper: A bigquery_helper object that specifies the connection to the stack overflow DB

    Outputs:
        results: A DataFrame with columns for user_id and number_of_answers. Follows similar logic to bigquery_experts_results shown above.
    '''
    my_query = \"""SELECT a.owner_user_id AS user_id, COUNT(1) AS number_of_answers
                  FROM `bigquery-public-data.stackoverflow.posts_questions` q
                        INNER JOIN `bigquery-public-data.stackoverflow.posts_answers` a
                        ON q.id = a.parent_Id
                  WHERE q.tags like '%' + tag + '%'
                  GROUP BY a.owner_user_id
                \"""
    # a real service would have good error handling for queries that scan too much data
    my_results = stack_overflow_helper.query_to_pandas_safe(my_query, max_gb_scanned=2)
    return my_results
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
