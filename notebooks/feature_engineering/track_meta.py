# See also examples/example_track/example_meta.py for a longer, commented example
track = dict(
    author_username='matleonard',
    course_name='Feature Engineering',
    course_url='https://www.kaggle.com/learn/feature-engineering'
)

lessons = [ {'topic': topic_name} for topic_name in
                    ['Baseline Model',
                    'Categorical Encodings',
                    'Feature Generation',
                    'Feature Selection']
            ]

notebooks = [
    # dict(
    #     filename='tut1.ipynb',
    #     lesson_idx=0,
    #     type='tutorial',
    #     ),
    # dict(
    #     filename='tut2.ipynb',
    #     lesson_idx=1,
    #     type='tutorial',
    #     ),
    dict(
        filename='ex1.ipynb',
        lesson_idx=0,
        type='exercise'
        # scriptid=1258954
    ),
    # dict(
    #     filename='tut3.ipynb',
    #     lesson_idx=2,
    #     type='tutorial'
    # ),
    dict(
        filename='ex2.ipynb',
        lesson_idx=1,
        type='exercise'
        # scriptid=400771
    ),
    # dict(
    #     filename='tut4.ipynb',
    #     lesson_idx=3,
    #     type='tutorial'
    # ),
    dict(
        filename='ex3.ipynb',
        lesson_idx=2,
        type='exercise'
        # scriptid=1259097
    ),
    # dict(
    #     filename='tut5.ipynb',
    #     lesson_idx=4,
    #     type='tutorial'
    #     ),
    dict(
        filename='ex4.ipynb',
        lesson_idx=3,
        type='exercise'
        # scriptid=1259126
        )
]

for nb in notebooks:
    nb['dataset_sources'] = ["matleonard/feature-engineering-data",
                             "dansbecker/nba-shot-logs"]
