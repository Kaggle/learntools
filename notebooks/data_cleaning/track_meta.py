track = dict(
    author_username='alexisbcook',
    course_name='Data Cleaning',
    course_url='https://www.kaggle.com/learn/data-cleaning',
    course_forum_url='https://www.kaggle.com/learn-forum/172650'
)

lessons = [ {'topic': topic_name} for topic_name in
                    ['Handling missing values',    #1
                     'Scaling and normalization',  #2
                     'Parsing dates',              #3
                     'Character encodings',        #4
                     'Inconsistent data entry']    #5
            ]

notebooks = [
    dict(
        filename='tut1.ipynb',
        lesson_idx=0,
        type='tutorial',
        dataset_sources=['maxhorowitz/nflplaybyplay2009to2016'],
        ),
    dict(
        filename='ex1.ipynb',
        lesson_idx=0,
        type='exercise',
        dataset_sources=['aparnashastry/building-permit-applications-data'],
        scriptid=10824396
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
        dataset_sources=['kemical/kickstarter-projects'],
        scriptid=10824404
    ),
    dict(
        filename='tut3.ipynb',
        lesson_idx=2,
        type='tutorial',
        dataset_sources=['nasa/landslide-events']
    ),
    dict(
        filename='ex3.ipynb',
        lesson_idx=2,
        type='exercise',
        dataset_sources=['usgs/earthquake-database', 'smithsonian/volcanic-eruptions'],
        scriptid=10824403
    ),
    dict(
        filename='tut4.ipynb',
        lesson_idx=3,
        type='tutorial',
        dataset_sources=['kemical/kickstarter-projects']
    ),
    dict(
        filename='ex4.ipynb',
        lesson_idx=3,
        type='exercise',
        dataset_sources=['kwullum/fatal-police-shootings-in-the-us'],
        scriptid=10824401
    ),
    dict(
        filename='tut5.ipynb',
        lesson_idx=4,
        type='tutorial',
        dataset_sources=['alexisbcook/pakistan-intellectual-capital']
        ),
    dict(
        filename='ex5.ipynb',
        lesson_idx=4,
        type='exercise',
        dataset_sources=['alexisbcook/pakistan-intellectual-capital'],
        scriptid=10824407
        ),
]