# See also examples/example_track/example_meta.py for a longer, commented example
track = dict(
    author_username='dansbecker',
    course_name='Introduction to Machine Learning',
    course_url='https://www.kaggle.com/learn/intro-to-machine-learning',
    course_forum_url='https://www.kaggle.com/learn-forum/161285'
)

lessons = [ {'topic': topic_name} for topic_name in
                    ['How Models Work',
                    'Basic Data Exploration',
                    'Your First Machine Learning Model',
                    'Model Validation',
                    'Underfitting and Overfitting',
                    'Random Forests',
                    'Machine Learning Competitions',
                    'Intro to AutoML',
                    'Getting Started with Titanic',]
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
        scriptid=1404276
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
    dict(filename='tut7.ipynb',
        lesson_idx=6,
        type='tutorial',
        author="alexisbcook"
        ),
    dict(
        filename='ex7.ipynb',
        lesson_idx=6,
        type='exercise',
        scriptid=1259198
        ),
#    dict(filename='tut8.ipynb',
#        lesson_idx=7,
#        type='tutorial'
#        ),
#    dict(filename='ex8.ipynb',
#        lesson_idx=7,
#        type='exercise',
#        scriptid=3685412
#        ),
    dict(
        filename='tut_automl.ipynb',
        lesson_idx=7,
        type='tutorial',
        enable_internet=True,
        author="alexisbcook"
        ),
    dict(
        filename='ex_automl.ipynb',
        lesson_idx=7,
        type='exercise',
        scriptid=10027938,
        author="alexisbcook"
        ),
    dict(filename='tut_titanic.ipynb',
        lesson_idx=8,
        type='tutorial',
        author="alexisbcook"
        ),
]

for nb in notebooks:
    nb['competition_sources'] = ["home-data-for-ml-course"]
    nb['dataset_sources'] = ["dansbecker/melbourne-housing-snapshot",
                             "iabhishekofficial/mobile-price-classification"]

    # ex7 is special case with only comp dataset, to allow submission from kernel
    if nb['filename'] == 'ex7.ipynb':
        nb['dataset_sources'] = []
        
    if nb['filename'] == 'tut_titanic.ipynb':
        nb['dataset_sources'] = []
        nb['competition_sources'] = ["titanic"]
        
    if nb['filename'] == 'tut_automl.ipynb':
        nb['competition_sources'] = ["new-york-city-taxi-fare-prediction"]
        nb['kernel_sources'] = ['alexisbcook/automl-tables-wrapper']
        nb['dataset_sources'] = []
        
    if nb['filename'] == 'ex_automl.ipynb':
        nb['competition_sources'] = ["house-prices-advanced-regression-techniques"]
        nb['kernel_sources'] = ['alexisbcook/automl-tables-wrapper']
        nb['dataset_sources'] = []
    
