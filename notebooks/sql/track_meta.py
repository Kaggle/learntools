# See also examples/example_track/example_meta.py for a longer, commented example
track = dict(
    author_username='dansbecker',
    course_name='SQL',
    course_url='https://www.kaggle.com/learn/intro-to-sql',
    course_forum_url='https://www.kaggle.com/learn-forum/161314'
)

lessons = [ {'topic': topic_name} for topic_name in
                    ['Getting Started with SQL and BigQuery',
                     'Select, From & Where',
                     'Group By, Having & Count',
                     'Order By',
                     'As & With',
                     'Joining Data',]
            ]

notebooks = [
    dict(
        filename='tut1.ipynb',
        lesson_idx=0,
        type='tutorial',
        dataset_sources = ["hacker-news/hacker-news"],
        ),
    dict(
        filename='ex1.ipynb',
        lesson_idx=0,
        type='exercise',
        dataset_sources = ["hacker-news/hacker-news", "chicago/chicago-crime"],
        scriptid=1058477
        ),
    dict(
        filename='tut2.ipynb',
        lesson_idx=1,
        type='tutorial',
        dataset_sources = ["hacker-news/hacker-news", "open-aq/openaq"],
    ),
    dict(
        filename='ex2.ipynb',
        lesson_idx=1,
        type='exercise',
        dataset_sources = ["hacker-news/hacker-news", "open-aq/openaq"],
        scriptid=681989,
        ),
    dict(
        filename='tut3.ipynb',
        lesson_idx=2,
        type='tutorial',
        dataset_sources = ["hacker-news/hacker-news"],
    ),
    dict(
        filename='ex3.ipynb',
        lesson_idx=2,
        type='exercise',
        dataset_sources = ["hacker-news/hacker-news"],
        scriptid=682058,
    ),
    dict(
        filename='tut4.ipynb',
        lesson_idx=3,
        type='tutorial',
        dataset_sources = ["usdot/nhtsa-traffic-fatalities"],
    ),
    dict(
        filename='ex4.ipynb',
        lesson_idx=3,
        type='exercise',
        dataset_sources = ["usdot/nhtsa-traffic-fatalities", "theworldbank/world-bank-intl-education"],
        scriptid=682087,
    ),
    dict(
        filename='tut5.ipynb',
        lesson_idx=4,
        type='tutorial',
        dataset_sources = ["bigquery/bitcoin-blockchain"],
    ),
    dict(
        filename='ex5.ipynb',
        lesson_idx=4,
        type='exercise',
        dataset_sources = ["chicago/chicago-taxi-trips-bq", "bigquery/bitcoin-blockchain"],
        scriptid=682113,
        enable_internet=True
 ),
    dict(
        filename='tut6.ipynb',
        lesson_idx=5,
        type='tutorial',
        dataset_sources = ["github/github-repos"],
        ),
    dict(filename='ex6.ipynb',
        lesson_idx=5,
        type='exercise',
        dataset_sources = ["stackoverflow/stackoverflow"],
        scriptid=682118,
        ),
]
