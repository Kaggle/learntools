import pandas as pd
from google.cloud import bigquery

from learntools.core import *

# Setup (1.88s on Kaggle)
client = bigquery.Client()

# (1) ProlificCommenters
prolific_commenters_query = """
                            SELECT author, COUNT(id) AS NumPosts
                            FROM `bigquery-public-data.hacker_news.comments`
                            GROUP BY author
                            HAVING COUNT(id) > 10000
                            """
query_job = client.query(prolific_commenters_query)
prolific_commenters_answer = query_job.to_dataframe()

# (2) NumDeletedPosts
deleted_posts_query = """
                      SELECT COUNT(1) AS num_deleted_posts
                      FROM `bigquery-public-data.hacker_news.comments`
                      WHERE deleted = True
                      """
query_job = client.query(deleted_posts_query)
deleted_posts = query_job.to_dataframe()
num_deleted_posts_answer = deleted_posts.values[0][0]

class ProlificCommenters(CodingProblem):
    _var = 'prolific_commenters'
    def check(self, results):
        assert(results.equals(prolific_commenters_answer)), ("The results don't look right. Try again.")
    _solution = CS(\
"""
prolific_commenters_query = \"""
                            SELECT author, COUNT(1) AS NumPosts
                            FROM `bigquery-public-data.hacker_news.comments`
                            GROUP BY author
                            HAVING COUNT(1) > 10000
                            \"""
""" 
)

class NumDeletedPosts(EqualityCheckProblem):
    _var = 'num_deleted_posts'
    _expected = num_deleted_posts_answer
    _solution = CS(\
"""
# Query to determine how many posts were deleted
deleted_posts_query = \"""
                      SELECT COUNT(1) AS num_deleted_posts
                      FROM `bigquery-public-data.hacker_news.comments`
                      WHERE deleted = True
                      \"""
                      
# Set up the query
query_job = client.query(deleted_posts_query, job_config=safe_config)

# API request - run the query, and return a pandas DataFrame
deleted_posts = query_job.to_dataframe()

# View results
print(deleted_posts)

num_deleted_posts = %d
""" % num_deleted_posts_answer
)

qvars = bind_exercises(globals(), [
    ProlificCommenters,
    NumDeletedPosts,
    ],
    tutorial_id=79,
    var_format='q_{n}',
    )

__all__ = list(qvars)
