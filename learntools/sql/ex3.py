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
        # check 1: column names
        assert set(results.columns.values) == set(['NumPosts', 'author']), ("The column names appear to be incorrect.  They should be `NumPosts` and `author`.")
        
        # check 2: pick a name. corresponding NumPosts matches solution?
        # get a name to check
        first_author = list(prolific_commenters_answer['author'])[0]
        # get corresponding NumPosts  
        correct_number = prolific_commenters_answer.loc[prolific_commenters_answer['author']==first_author]['NumPosts'].values[0]
        # want this to equal the corresponding NumPosts above
        check_number = results.loc[results['author']==first_author]['NumPosts'].values[0]
        assert(int(check_number)==int(correct_number)), ("The results don't look right. Try again.")

        # check 3: check count > 10000
        assert(all(results['NumPosts'].values>10000)), ("Only select authors with more than 10,000 posts.")
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
query_job = client.query(deleted_posts_query)

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
    var_format='q_{n}',
    )

__all__ = list(qvars)
