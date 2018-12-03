# See also examples/example_track/example_meta.py for a longer, commented example
track = dict(
    author_username='dansbecker',
    course_name='Machine Learning',
    course_url='https://www.kaggle.com/learn/machine-learning'
)

lessons = [ {'topic': topic_name} for topic_name in
                    ['How Models Work',
                    'Basic Data Exploration',
                    'Your First Machine Learning Model',
                    'Model Validation',
                    'Underfitting and Overfitting',
                    'Random Forests',
                    'Machine Learning Competitions',]
            ]

notebooks = [
    dict(
        filename='tut1.ipynb',
        lesson_idx=0,
        type='tutorial',
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
        scriptid=1258954
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
        scriptid=400771
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
        scriptid=1259097
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
        scriptid=1259126
        ),
    dict(filename='tut6.ipynb',
        lesson_idx=5,
        type='tutorial'
        ),
    dict(
        filename='ex6.ipynb',
        lesson_idx=5,
        type='exercise',
        scriptid=1259186
        ),
    dict(
        filename='ex7.ipynb',
        lesson_idx=6,
        type='exercise',
        scriptid=1259198
        ),
]

for nb in notebooks:
    nb['competition_sources'] = ["home-data-for-ml-course"]
    nb['dataset_sources'] = ["dansbecker/melbourne-housing-snapshot"]

    # ex7 is special case with only comp dataset, to allow submission from kernel
    if nb['filename'] == 'ex7.ipynb':
        nb['dataset_sources'] = []
