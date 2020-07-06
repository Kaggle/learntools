# See also examples/example_track/example_meta.py for a longer, commented example
track = dict(
    author_username='matleonard',
    course_name='Feature Engineering',
    course_url='https://www.kaggle.com/learn/feature-engineering',
    course_forum_url='https://www.kaggle.com/learn-forum/161443'
)

lessons = [ {'topic': topic_name} for topic_name in
                    ['Baseline Model',
                    'Categorical Encodings',
                    'Feature Generation',
                    'Feature Selection']
            ]

notebooks = [
    dict(
        filename='tut1.ipynb',
        lesson_idx=0,
        type='tutorial',
        ),
    dict(
        filename='ex1.ipynb',
        lesson_idx=0,
        type='exercise',
        scriptid=5407496
    ),
    dict(
        filename='tut2.ipynb',
        lesson_idx=1,
        type='tutorial'
    ),
    dict(
        filename='ex2.ipynb',
        lesson_idx=1,
        type='exercise',
        scriptid=5407502
    ),
    dict(
        filename='tut3.ipynb',
        lesson_idx=2,
        type='tutorial'
    ),
    dict(
        filename='ex3.ipynb',
        lesson_idx=2,
        type='exercise',
        scriptid=5407501
    ),
    dict(
        filename='tut4.ipynb',
        lesson_idx=3,
        type='tutorial'
        ),
    dict(
        filename='ex4.ipynb',
        lesson_idx=3,
        type='exercise',
        scriptid=5407500
        )
]

for nb in notebooks:
    nb['dataset_sources'] = ["matleonard/feature-engineering-data",
                             "kemical/kickstarter-projects"]
