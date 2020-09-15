track = dict(
    author_username='alexisbcook',
    course_name='Intermediate Machine Learning',
    course_url='https://www.kaggle.com/learn/intermediate-machine-learning',
    course_forum_url='https://www.kaggle.com/learn-forum/161289'
)

lessons = [ {'topic': topic_name} for topic_name in
                    ['Introduction',         #1
                    'Missing Values',        #2
                    'Categorical Variables', #3
                    'Pipelines',             #4
                    'Cross-Validation',      #5
                    'XGBoost',               #6
                    'Data Leakage',]         #7
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
        scriptid=3370272
    ),
    dict(
        filename='tut2.ipynb',
        lesson_idx=1,
        type='tutorial',
        ),
    dict(
        filename='ex2.ipynb',
        lesson_idx=1,
        type='exercise',
        scriptid=3370280
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
        scriptid=3370279
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
        scriptid=3370278
    ),
    dict(
        filename='tut5.ipynb',
        lesson_idx=4,
        type='tutorial'
        ),
    dict(
        filename='ex5.ipynb',
        lesson_idx=4,
        type='exercise',
        scriptid=3370281
        ),
    dict(filename='tut6.ipynb',
        lesson_idx=5,
        type='tutorial'
        ),
    dict(
        filename='ex6.ipynb',
        lesson_idx=5,
        type='exercise',
        scriptid=3370271
        ),
    dict(filename='tut7.ipynb',
        lesson_idx=6,
        type='tutorial'
        ),
    dict(
        filename='ex7.ipynb',
        lesson_idx=6,
        type='exercise',
        scriptid=3370270
        ),
]

for nb in notebooks:
    nb['competition_sources'] = ["home-data-for-ml-course"]
    nb['dataset_sources'] = ["dansbecker/melbourne-housing-snapshot", 
                             "dansbecker/aer-credit-card-data"]

    # exercises are special case with only comp dataset, to allow submission from kernel
    if "ex" in nb['filename']:
        nb['dataset_sources'] = []
